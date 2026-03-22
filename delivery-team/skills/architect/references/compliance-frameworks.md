# Compliance Frameworks Reference

## SOC 2 Trust Service Principles

### Security (Common Criteria)
- **CC1**: Control Environment -- governance, ethical values, oversight structure
- **CC2**: Communication & Information -- internal/external communication of policies
- **CC3**: Risk Assessment -- identify and analyze risks to objectives
- **CC5**: Control Activities -- policies and procedures to mitigate risks
- **CC6**: Logical & Physical Access -- restrict access to authorized users
- **CC7**: System Operations -- detect and respond to anomalies
- **CC8**: Change Management -- authorized, tested, approved changes only
- **CC9**: Risk Mitigation -- identify and mitigate business disruption risks

### Availability
- System uptime commitments and SLA documentation
- Disaster recovery and business continuity plans
- Capacity planning and monitoring procedures
- Incident response for availability events

### Processing Integrity
- Data processing is complete, valid, accurate, and timely
- Error detection and correction mechanisms
- Input validation and output reconciliation
- Processing monitoring and quality assurance

### Confidentiality
- Classification of confidential information (public, internal, confidential, restricted)
- Encryption of confidential data at rest and in transit
- Access restrictions based on classification level
- Secure disposal procedures for confidential data

### Privacy
- Notice and consent for personal information collection
- Choice and consent mechanisms for data use
- Collection limited to stated purposes
- Retention and disposal aligned with stated policies
- Access rights for data subjects

---

## ISO 27001 Control Families (Annex A Summary)

| Family | Domain | Key Controls |
|--------|--------|-------------|
| A.5 | Information Security Policies | Policy document, management review cadence |
| A.6 | Organization of Info Security | Roles, responsibilities, segregation of duties, mobile/telework |
| A.7 | Human Resource Security | Screening, terms of employment, awareness training, termination |
| A.8 | Asset Management | Asset inventory, acceptable use, classification, media handling |
| A.9 | Access Control | Access policy, user registration, privilege management, password policy |
| A.10 | Cryptography | Encryption policy, key management lifecycle |
| A.11 | Physical & Environmental | Secure areas, equipment protection, clear desk/screen |
| A.12 | Operations Security | Documented procedures, malware protection, backup, logging, patching |
| A.13 | Communications Security | Network controls, segregation, information transfer policies |
| A.14 | System Acquisition & Development | Security requirements in SDLC, secure development policy, test data |
| A.15 | Supplier Relationships | Supplier security policy, supply chain risk, monitoring/review |
| A.16 | Incident Management | Responsibilities, reporting, response, evidence collection, lessons learned |
| A.17 | Business Continuity | Planning, implementation, verification of continuity controls |
| A.18 | Compliance | Legal requirements identification, IP protection, privacy, audit |

---

## HIPAA Safeguards

### Administrative Safeguards
- Security management process (risk analysis, risk management, sanctions, review)
- Assigned security responsibility (designated security officer)
- Workforce security (authorization, clearance, termination procedures)
- Information access management (access authorization, establishment, modification)
- Security awareness training (reminders, malware protection, login monitoring, password management)
- Contingency plan (data backup, disaster recovery, emergency mode operations, testing)
- Evaluation (periodic technical and non-technical evaluation)

### Physical Safeguards
- Facility access controls (contingency operations, facility security plan, visitor access, maintenance records)
- Workstation use and security (policies for use, physical safeguards)
- Device and media controls (disposal, reuse, accountability, data backup)

### Technical Safeguards
- Access control (unique user ID, emergency access, automatic logoff, encryption/decryption)
- Audit controls (hardware/software/procedural mechanisms for recording access)
- Integrity controls (mechanisms to authenticate ePHI, error detection)
- Transmission security (integrity controls, encryption for data in transit)
- Authentication (verify identity of persons seeking access to ePHI)

---

## PCI DSS Requirements (v4.0)

### Build and Maintain a Secure Network
1. Install and maintain network security controls
2. Apply secure configurations to all system components

### Protect Account Data
3. Protect stored account data (encryption, masking, truncation)
4. Protect cardholder data with strong cryptography during transmission

### Maintain a Vulnerability Management Program
5. Protect all systems and networks from malicious software
6. Develop and maintain secure systems and software

### Implement Strong Access Control Measures
7. Restrict access to system components by business need-to-know
8. Identify users and authenticate access to system components
9. Restrict physical access to cardholder data

### Regularly Monitor and Test Networks
10. Log and monitor all access to system components and cardholder data
11. Test security of systems and networks regularly

### Maintain an Information Security Policy
12. Support information security with organizational policies and programs

---

## Audit Evidence Patterns

### What Auditors Look For
- **Policy existence**: Written, approved, and distributed policies
- **Policy enforcement**: Evidence that policies are followed (logs, tickets, sign-offs)
- **Consistency**: Controls operating the same way over the audit period
- **Completeness**: No gaps in coverage -- all systems, all users, all time periods
- **Timeliness**: Reviews and approvals happen within defined timeframes

### Evidence Collection Methods
- **Automated**: System-generated logs, configuration exports, scan results
- **Manual**: Screenshots, sign-off sheets, meeting minutes, approval emails
- **Inquiry**: Interviews with process owners, walkthroughs of procedures
- **Observation**: Auditor witnesses the control in operation

### Documentation Requirements
- Version-controlled policy documents with approval history
- Change management records with approvals and testing evidence
- Access review logs with remediation actions for exceptions
- Training completion records with content and attendee lists
- Incident reports with response timelines and resolution details

---

## Cross-Framework Control Mapping

| Control Area | SOC 2 | ISO 27001 | HIPAA | PCI DSS |
|-------------|-------|-----------|-------|---------|
| Access Control | CC6.1-CC6.8 | A.9 | Technical Safeguards | Req 7, 8 |
| Encryption | CC6.1, CC6.7 | A.10 | Technical Safeguards | Req 3, 4 |
| Logging/Monitoring | CC7.1-CC7.4 | A.12 | Audit Controls | Req 10 |
| Incident Response | CC7.3-CC7.5 | A.16 | Administrative Safeguards | Req 12.10 |
| Change Management | CC8.1 | A.12, A.14 | Administrative Safeguards | Req 6 |
| Risk Assessment | CC3.1-CC3.4 | A.6, A.18 | Administrative Safeguards | Req 12.2 |
| Physical Security | CC6.4-CC6.5 | A.11 | Physical Safeguards | Req 9 |
| Vendor Management | CC9.2 | A.15 | Business Associate Agreements | Req 12.8 |
| Training | CC1.4 | A.7 | Administrative Safeguards | Req 12.6 |
| Business Continuity | CC9.1 | A.17 | Contingency Plan | Req 12.10 |

---

## Compliance Program Structure

### Hierarchy
1. **Policies** -- High-level statements of intent and direction (approved by leadership)
2. **Standards** -- Mandatory requirements that implement policies (specific and measurable)
3. **Procedures** -- Step-by-step instructions for carrying out standards
4. **Guidelines** -- Recommended practices (non-mandatory but encouraged)

### Policy Lifecycle
- Draft with stakeholder input
- Legal and compliance review
- Management approval and sign-off
- Communication and training
- Annual review and update cycle
- Version control and distribution tracking

### Compliance Monitoring
- Continuous controls monitoring (automated where possible)
- Periodic internal audits (quarterly or semi-annually)
- Annual external audits (SOC 2 Type II, ISO certification)
- Exception tracking and remediation with defined SLAs
- Compliance metrics dashboard (control effectiveness, exception rate, remediation time)
