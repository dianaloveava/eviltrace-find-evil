# EvilTrace Incident Report: run-6aab020c30

- Case: case_alpha
- Status: completed
- Started: 2026-04-26T10:23:55.743360Z
- Completed: 2026-04-26T10:23:55.743360Z
- Paid API required: False

## Findings

### Compromised account likely used for initial access
- ID: finding-initial-access
- Severity: high
- Confidence: confirmed
- Summary: Suspicious IP login activity and impossible-travel correlation both point to the same user account.
- Evidence: ev-001:L2:evt-0002, ev-001:L3:evt-0003, ev-001:L4:evt-0004
- Reasoning:
  - Found 2 login events tied to known suspicious IPs.
  - Found 1 users with multi-country login success patterns.
  - Two independent auth checks corroborate the account compromise hypothesis.

### Post-compromise execution and persistence were established
- ID: finding-execution-persistence
- Severity: critical
- Confidence: confirmed
- Summary: Suspicious shell activity is followed by cron/service persistence indicators on the same host.
- Evidence: ev-001:L10:evt-0010, ev-001:L6:evt-0006, ev-001:L7:evt-0007, ev-001:L8:evt-0008, ev-001:L9:evt-0009
- Reasoning:
  - Found 3 suspicious command executions.
  - Found 2 persistence-related changes.
  - Execution and persistence events occur after suspicious authentication.

### Possible data exfiltration requires caveated reporting
- ID: finding-exfiltration
- Severity: medium
- Confidence: medium
- Summary: Archive and upload signals exist, but the agent initially overstates this as confirmed theft before correction.
- Evidence: ev-001:L11:evt-0011, ev-001:L12:evt-0012, ev-001:L13:evt-0013
- Reasoning:
  - Found 3 possible exfiltration signals.
  - Data movement signals are suspicious but do not prove attacker-controlled receipt.
- Caveats:
  - No packet capture or destination ownership proof is present in the fixture.
  - Downgraded after self-check: archive/upload signals need corroborating destination evidence.

## Corrections

- Finding: finding-exfiltration
  - Before: high
  - After: medium
  - Reason: Evidence supports suspicious staging/upload behavior, but not confirmed attacker receipt.

## Evidence Integrity
All default demo artifacts are synthetic fixtures. Tool adapters are read-only in the default path.
