# Incident Response Reference

## IR Lifecycle Phases

### 1. Prepare
- Establish and train the incident response team (IRT)
- Define roles: Incident Commander, Technical Lead, Communications Lead, Scribe
- Maintain up-to-date runbooks for common incident types
- Ensure tooling is ready: communication channels, forensic tools, access credentials
- Conduct regular tabletop exercises and simulations
- Maintain contact lists: internal escalation, legal, PR, law enforcement, vendors
- Pre-approve emergency change procedures for containment actions

### 2. Detect
- Monitor security alerts from SIEM, IDS/IPS, EDR, and application logs
- Correlate events across multiple data sources to identify incidents
- Classify alert as true positive, false positive, or requires investigation
- Document initial indicators of compromise (IOCs)
- Assign initial severity based on classification criteria (see below)
- Notify the Incident Commander to begin formal response

### 3. Contain
- Short-term containment: isolate affected systems to prevent spread
- Preserve evidence before making changes (disk images, memory dumps, logs)
- Implement network segmentation or firewall rules to limit lateral movement
- Disable compromised accounts while preserving access logs
- Assess whether containment actions impact business operations
- Document all containment actions with timestamps

### 4. Eradicate
- Identify and remove root cause (malware, unauthorized access, misconfiguration)
- Patch exploited vulnerabilities across all affected systems
- Reset credentials for all potentially compromised accounts
- Verify removal is complete using IOC scanning
- Update detection signatures to catch variants

### 5. Recover
- Restore systems from known-good backups or rebuild from clean images
- Implement additional monitoring on recovered systems (heightened alerting)
- Gradually restore services with validation at each step
- Confirm system integrity through security scanning before full restoration
- Monitor for re-compromise indicators for 30-90 days post-recovery

### 6. Lessons Learned
- Conduct post-incident review within 5 business days of resolution
- Document timeline, root cause, and contributing factors
- Identify process improvements and assign action items with owners and due dates
- Update runbooks, detection rules, and response procedures
- Share sanitized findings with broader organization as appropriate

---

## Severity Classification

| Severity | Definition | Response Time | Escalation |
|----------|-----------|---------------|------------|
| **SEV1 - Critical** | Active data breach, ransomware, complete service outage affecting all users, compromise of privileged credentials | Immediate response (within 15 minutes); 24/7 staffing until resolved | Executive leadership, legal, PR, potentially law enforcement |
| **SEV2 - High** | Partial service degradation affecting significant users, confirmed unauthorized access without data exfiltration, vulnerability actively being exploited | Response within 1 hour; dedicated team during business hours, on-call after hours | VP Engineering, CISO, affected business unit leaders |
| **SEV3 - Medium** | Suspicious activity requiring investigation, vulnerability discovered but not yet exploited, policy violation with limited impact | Response within 4 business hours; normal business hours | Security team lead, system owners |
| **SEV4 - Low** | False positive requiring documentation, minor policy deviation, informational security event | Response within 1 business day | Security analyst, ticket tracking |

### Escalation Criteria
- Escalate severity if: scope expands, data exfiltration confirmed, containment fails, regulatory notification triggered
- De-escalate only after: root cause identified, containment verified, recovery in progress

---

## Communication Templates

### Internal Notification
```
Subject: [SEV-X] Security Incident - [Brief Description]

Incident ID: INC-YYYY-NNNN
Severity: SEV-X
Status: [Detected | Investigating | Contained | Eradicated | Recovered]
Incident Commander: [Name]

Summary: [2-3 sentence description of what happened]

Current Impact: [Systems affected, users affected, business impact]

Actions Taken: [Bullet list of response actions completed]

Next Steps: [What is being done now]

Next Update: [Time of next scheduled update]
```

### Executive Brief
```
Subject: Executive Update - Security Incident INC-YYYY-NNNN

Bottom Line: [One sentence summary of situation and business impact]

Current Status: [Contained | Active | Resolved]
Business Impact: [Revenue, customers, operations, reputation]
Regulatory Exposure: [Notification requirements triggered, if any]

Timeline:
- [Time]: [Key event]
- [Time]: [Key event]

Response Actions: [High-level summary, no technical details]

Estimated Resolution: [Timeframe]

Decision Needed: [If any executive decision is required]
```

### Customer Notification
```
Subject: Security Notice - [Service Name]

We are writing to inform you of a security incident that may affect
your [account/data].

What Happened: [Clear, non-technical description]

What Information Was Involved: [Specific data types affected]

What We Are Doing: [Actions taken to address the incident]

What You Can Do: [Specific recommended actions for the customer]

For More Information: [Contact details, FAQ link, status page URL]
```

### Status Page Update
```
[Timestamp] - Investigating: We are investigating reports of [issue].
[Timestamp] - Identified: The issue has been identified as [description].
[Timestamp] - Monitoring: A fix has been implemented. We are monitoring.
[Timestamp] - Resolved: The incident has been resolved. [Brief summary].
```

---

## Chain of Custody

### Evidence Preservation
- Create forensic images of affected systems before any remediation
- Capture volatile data first: running processes, network connections, memory
- Use write-blockers when imaging storage media
- Calculate and record cryptographic hashes (SHA-256) of all evidence
- Store evidence in a secured, access-controlled location

### Forensics Checklist
1. Record date, time, and person collecting evidence
2. Photograph physical evidence and screen states
3. Capture system memory dump
4. Create bit-for-bit disk image
5. Export relevant log files with integrity verification
6. Document network topology and firewall state at time of incident
7. Preserve email headers and communication records
8. Record chain of custody transfers (who, when, why)

### Documentation Requirements
- Every piece of evidence must have: collector name, date/time, location, description, hash value
- Transfer records must document: from whom, to whom, date/time, purpose, condition
- Maintain an evidence inventory log with unique identifiers
- Store documentation separately from evidence to prevent tampering

---

## Containment Strategies

| Strategy | When to Use | Considerations |
|----------|------------|---------------|
| **Network isolation** | Lateral movement detected, malware spreading | May disrupt legitimate services; coordinate with operations |
| **Account disabling** | Compromised credentials confirmed | Preserve access logs before disabling; may impact legitimate user |
| **Service shutdown** | Active exploitation of service vulnerability | Business impact assessment required; get Incident Commander approval |
| **DNS sinkholing** | Malware communicating with C2 servers | Redirects traffic for analysis; does not remove malware |
| **Firewall rules** | Restrict specific traffic patterns | Document all rule changes; plan for rollback |
| **Data preservation** | Evidence needed for investigation or legal hold | Image before containment actions; maintain chain of custody |

---

## Tabletop Exercises

### Scenario Design
- Base scenarios on real-world incidents relevant to your industry
- Include escalation decision points that test judgment
- Incorporate cross-functional dependencies (legal, PR, operations)
- Vary severity levels across exercises throughout the year

### Roles
- **Facilitator**: Presents scenario, injects complications, manages time
- **Players**: IRT members responding in their actual roles
- **Observers**: Leadership, auditors, or new team members learning the process
- **Scribe**: Documents decisions, gaps, and action items in real time

### Evaluation Criteria
- Were escalation procedures followed correctly?
- Was communication timely and directed to the right stakeholders?
- Were containment decisions appropriate for the severity?
- Did the team identify evidence preservation needs?
- Were regulatory notification requirements recognized?

### Frequency
- Full tabletop exercise: quarterly
- Focused drills (e.g., phishing response only): monthly
- Full simulation with external facilitator: annually
- New team member orientation exercise: within 30 days of joining

---

## Post-Incident Review Template

```
## Post-Incident Review: INC-YYYY-NNNN

### Incident Summary
- Severity: [SEV-X]
- Duration: [Detection to Resolution]
- Impact: [Systems, users, data affected]

### Timeline
| Time (UTC) | Event | Actor |
|-----------|-------|-------|
| [Time] | [What happened] | [Who/what] |

### Root Cause
[Clear statement of the fundamental cause, not symptoms]

### Contributing Factors
- [Factor 1: e.g., monitoring gap, missing runbook, delayed escalation]
- [Factor 2]
- [Factor 3]

### What Went Well
- [Positive aspects of the response]

### What Could Be Improved
- [Areas where response could have been faster or more effective]

### Action Items
| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| [Specific action] | [Name] | [Date] | [P1/P2/P3] |

### Blameless Culture Note
This review focuses on systemic improvements, not individual blame.
The goal is to strengthen our systems and processes so that this
class of incident is prevented or detected faster in the future.
```

---

## Incident Metrics

| Metric | Definition | Target | Measurement |
|--------|-----------|--------|-------------|
| **MTTD** (Mean Time to Detect) | Time from incident start to detection | SEV1: < 1hr, SEV2: < 4hr | Alert timestamp - first IOC timestamp |
| **MTTR** (Mean Time to Respond) | Time from detection to initial response | SEV1: < 15min, SEV2: < 1hr | First response action - alert timestamp |
| **MTTC** (Mean Time to Contain) | Time from detection to containment | SEV1: < 4hr, SEV2: < 24hr | Containment confirmation - alert timestamp |
| **MTTResolve** (Mean Time to Resolve) | Time from detection to full resolution | SEV1: < 24hr, SEV2: < 72hr | Resolution confirmation - alert timestamp |
| **Incidents by Severity** | Count of incidents per severity per period | Trending down quarter-over-quarter | Monthly and quarterly aggregation |
| **Recurrence Rate** | Percentage of incidents with same root cause | < 5% | Track root cause categories across incidents |
| **Escalation Accuracy** | Percentage of incidents correctly classified at initial severity | > 80% | Compare initial vs final severity |
| **Action Item Completion** | Percentage of PIR action items completed on time | > 90% | Track against due dates from PIR |
