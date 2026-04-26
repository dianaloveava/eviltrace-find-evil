import json
import tempfile
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from threading import Thread

from eviltrace.agent import InvestigationAgent, render_markdown_report
from eviltrace.evidence import inventory_case, load_events
from eviltrace.server import ThreadingHTTPServer, EvilTraceHandler
from eviltrace.tools import ReadOnlyToolbox

from eviltrace.importers import normalize_sift_exports
from eviltrace.tool_server import call_tool


class EvidenceTests(unittest.TestCase):
    def test_inventory_hashes_fixture(self):
        records = inventory_case('case_alpha')
        self.assertGreaterEqual(len(records), 2)
        event_record = next(record for record in records if record.path.endswith('events.jsonl'))
        self.assertEqual(len(event_record.sha256), 64)
        self.assertEqual(event_record.kind, 'event-log')

    def test_events_have_evidence_refs(self):
        evidence = inventory_case('case_alpha')
        events = load_events('case_alpha', evidence)
        self.assertGreaterEqual(len(events), 10)
        self.assertTrue(all(event.evidence_id for event in events))
        self.assertTrue(all(event.line > 0 for event in events))


class ToolboxTests(unittest.TestCase):
    def setUp(self):
        evidence = inventory_case('case_alpha')
        self.tools = ReadOnlyToolbox(load_events('case_alpha', evidence))

    def test_tools_detect_suspicious_activity(self):
        self.assertGreater(len(self.tools.suspicious_logins().evidence_refs), 0)
        self.assertGreater(len(self.tools.suspicious_commands().evidence_refs), 0)
        self.assertGreater(len(self.tools.persistence_changes().evidence_refs), 0)
        self.assertGreater(len(self.tools.exfil_signals().evidence_refs), 0)


class AgentTests(unittest.TestCase):
    def test_agent_run_has_correction_and_evidence_linked_findings(self):
        run = InvestigationAgent('case_alpha').run()
        self.assertEqual(run.status, 'completed')
        self.assertGreaterEqual(len(run.findings), 3)
        self.assertGreaterEqual(len(run.corrections), 1)
        self.assertTrue(all(finding.evidence_refs for finding in run.findings))
        exfil = next(f for f in run.findings if f.id == 'finding-exfiltration')
        self.assertEqual(exfil.confidence, 'medium')
        self.assertFalse(run.metrics['paid_api_required'])

    def test_report_exports_markdown(self):
        run = InvestigationAgent('case_alpha').run()
        report = render_markdown_report(run)
        self.assertIn('# EvilTrace Incident Report', report)
        self.assertIn('Evidence Integrity', report)
        self.assertIn('finding-exfiltration', report)


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), EvilTraceHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_post_run_and_fetch_report(self):
        base = f'http://127.0.0.1:{self.port}'
        req = Request(base + '/api/runs', method='POST')
        with urlopen(req, timeout=10) as response:
            payload = json.loads(response.read().decode('utf-8'))
        self.assertEqual(payload['status'], 'completed')
        with urlopen(base + '/api/runs/latest/report.md', timeout=10) as response:
            report = response.read().decode('utf-8')
        self.assertIn('Corrections', report)


class SiftImportTests(unittest.TestCase):
    def test_import_sift_exports_and_call_readonly_tool(self):
        dest = normalize_sift_exports('data/sift_exports/demo', 'sift_demo_test')
        self.assertTrue((dest / 'events.jsonl').exists())
        result = call_tool('suspicious_commands', 'sift_demo_test')
        self.assertGreaterEqual(len(result['evidence_refs']), 1)
        inventory = call_tool('inventory_case', 'sift_demo_test')
        self.assertGreaterEqual(len(inventory['evidence']), 1)


if __name__ == '__main__':
    unittest.main()
