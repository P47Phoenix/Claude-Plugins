# Privacy Patterns Reference

## GDPR Key Articles Mapped to Technical Controls

### Article 5: Principles of Processing
| Principle | Technical Control |
|-----------|-----------------|
| Lawfulness, fairness, transparency | Consent management system; privacy notices served at collection points |
| Purpose limitation | Enforce data usage through access control policies tied to stated purposes |
| Data minimization | Collect only fields required for stated purpose; review and prune data models |
| Accuracy | Provide self-service data correction; implement validation at input |
| Storage limitation | Automated retention enforcement; scheduled deletion jobs per data category |
| Integrity and confidentiality | Encryption at rest and in transit; access logging; integrity checks |
| Accountability | Audit trails; processing activity records; data protection impact assessments |

### Article 6: Lawful Basis for Processing
- **Consent**: Freely given, specific, informed, unambiguous; must be withdrawable
- **Contract**: Processing necessary for contract performance
- **Legal obligation**: Processing required by law
- **Vital interests**: Processing to protect someone's life
- **Public interest**: Processing for public interest tasks
- **Legitimate interests**: Balanced against data subject rights (requires LIA)

Document the lawful basis for every processing activity in a processing register.

### Articles 13-14: Transparency
- Provide identity of controller and DPO contact at point of collection
- State purposes and lawful basis for each processing activity
- Disclose recipients or categories of recipients
- Inform of international transfers and safeguards
- State retention periods or criteria for determining them
- Inform data subjects of their rights under Articles 15-22

### Articles 15-20: Data Subject Rights
| Right | Technical Implementation |
|-------|------------------------|
| Right of Access (Art. 15) | API or portal for data export; respond within 30 days |
| Right to Rectification (Art. 16) | Self-service data editing; admin correction workflow |
| Right to Erasure (Art. 17) | Deletion cascade across all systems; backup handling |
| Right to Restrict Processing (Art. 18) | Flag mechanism to suppress processing while retaining data |
| Right to Data Portability (Art. 20) | Export in structured, machine-readable format (JSON, CSV) |
| Right to Object (Art. 21) | Opt-out mechanism for direct marketing; processing cessation |

### Article 25: Privacy by Design and Default
- Implement data protection measures from the design phase
- Default settings must be the most privacy-protective option
- Process only data necessary for each specific purpose by default
- Data should not be made accessible to an indefinite number of persons by default

### Article 32: Security of Processing
- Pseudonymization and encryption of personal data
- Ability to ensure ongoing confidentiality, integrity, availability, and resilience
- Ability to restore access to personal data in a timely manner after an incident
- Regular testing, assessing, and evaluating effectiveness of security measures

### Articles 33-34: Breach Notification
- Notify supervisory authority within 72 hours of becoming aware of a breach
- Notify affected data subjects without undue delay if high risk to rights/freedoms
- Document all breaches regardless of notification requirement (breach register)
- Include: nature of breach, categories/numbers affected, likely consequences, measures taken

### Article 35: Data Protection Impact Assessment (DPIA)
- Required when processing likely results in high risk to individuals
- Required for: systematic monitoring, large-scale special category data, automated decision-making
- Must describe processing, assess necessity/proportionality, identify risks, define mitigations

---

## CCPA/CPRA Requirements

### Right to Know
- Disclose categories and specific pieces of personal information collected
- Disclose sources, purposes, and third parties with whom data is shared
- Respond to verifiable consumer requests within 45 days
- Provide information for the 12-month period preceding the request

### Right to Delete
- Delete personal information upon verified consumer request
- Direct service providers to delete as well
- Exceptions: complete transactions, detect security incidents, comply with legal obligations
- Confirm deletion to the consumer

### Right to Opt-Out (Do Not Sell/Share)
- Provide a "Do Not Sell or Share My Personal Information" link
- Process opt-out requests without requiring account creation
- Respect Global Privacy Control (GPC) browser signals
- Wait at least 12 months before requesting consent to sell again

### CPRA Additions
- Right to correct inaccurate personal information
- Right to limit use of sensitive personal information
- Automated decision-making transparency and opt-out
- Data minimization and purpose limitation requirements
- Mandatory risk assessments for high-risk processing

---

## Data Minimization Patterns

### Collection Minimization
- Audit every data field: justify why it is needed for the stated purpose
- Use progressive profiling: collect only what is needed at each interaction
- Anonymize or pseudonymize data at the point of collection when full identity is not needed
- Avoid collecting data "just in case" -- speculative collection violates minimization

### Purpose Limitation
- Bind each data element to one or more documented purposes
- Implement technical controls that prevent data use outside stated purposes
- Require new purpose justification and consent before repurposing existing data
- Log purpose of access alongside access events for auditability

### Storage Limitation
- Define retention periods for each data category based on legal and business requirements
- Implement automated deletion or anonymization at retention expiry
- Review retention schedules annually for continued appropriateness
- Separate long-term analytical data from operational data using aggregation/anonymization

---

## Consent Management

### Explicit Consent Requirements
- Consent must be a clear affirmative action (no pre-ticked boxes)
- Separate consent for each distinct processing purpose
- Present consent request in clear, plain language
- Record: who consented, when, what they were told, how they consented

### Granular Options
- Allow users to consent to specific processing purposes independently
- Provide a consent dashboard for reviewing and modifying preferences
- Support partial consent (accept some purposes, reject others)
- Distinguish between required consent (contractual) and optional consent

### Withdrawal Mechanism
- Withdrawal must be as easy as giving consent
- Process withdrawal without undue delay
- Cease processing based on withdrawn consent immediately
- Retain record of consent and withdrawal for audit purposes

### Consent Audit Trail
- Store consent records immutably (append-only log or blockchain-anchored hash)
- Record: consent version, timestamp, user identifier, IP address, consent text shown
- Maintain ability to demonstrate what each user consented to at any point in time
- Retain consent records for the duration of processing plus legal retention period

---

## DPIA Template

```
## Data Protection Impact Assessment

### 1. Processing Description
- Nature: [What processing is being done]
- Scope: [Volume of data, number of subjects, geographic scope]
- Context: [Relationship with data subjects, their expectations]
- Purpose: [Why this processing is necessary]

### 2. Necessity and Proportionality
- Lawful basis for processing: [Art. 6 basis]
- Is the processing necessary for the purpose? [Justification]
- Could the purpose be achieved with less data? [Analysis]
- How is data quality ensured? [Measures]

### 3. Risk Identification
| Risk | Likelihood | Severity | Risk Level |
|------|-----------|----------|------------|
| [Unauthorized access to personal data] | [Low/Med/High] | [Low/Med/High] | [Score] |
| [Data loss or corruption] | [Low/Med/High] | [Low/Med/High] | [Score] |
| [Excessive data collection] | [Low/Med/High] | [Low/Med/High] | [Score] |
| [Inability to exercise rights] | [Low/Med/High] | [Low/Med/High] | [Score] |

### 4. Mitigation Measures
| Risk | Mitigation | Residual Risk |
|------|-----------|---------------|
| [Risk] | [Technical or organizational measure] | [Acceptable/Needs review] |

### 5. Approval
- DPO Consultation: [Date, outcome]
- Supervisory Authority Consultation: [If required]
- Approval: [Authorized signatory, date]
```

---

## Data Retention Policies

### Retention Schedule by Data Type
| Data Category | Retention Period | Basis | Deletion Method |
|--------------|-----------------|-------|----------------|
| Active user account data | Duration of account + 30 days | Contract | Automated deletion pipeline |
| Transaction records | 7 years | Legal (tax/financial regulations) | Secure deletion after period |
| Server access logs | 90 days | Legitimate interest (security) | Automated log rotation |
| Marketing consent records | Duration of consent + 3 years | Legal (demonstrate compliance) | Archive then delete |
| Support tickets | 2 years after resolution | Legitimate interest | Anonymization |
| Analytics data | 26 months (aggregated) | Consent | Aggregation removes personal data |
| Backup data | 90 days rolling | Legitimate interest (recovery) | Overwritten by rotation |

### Deletion Procedures
- Verify no legal hold applies before deletion
- Execute deletion across all systems (primary, replicas, caches, search indexes)
- Confirm deletion with automated verification check
- Log deletion event for audit trail (what was deleted, when, by what process)

### Legal Hold
- Legal hold suspends normal retention/deletion for data relevant to litigation
- Implement technical controls to prevent deletion of held data
- Scope holds narrowly to avoid over-preservation
- Release holds promptly when legal matter concludes

---

## Right to Erasure Implementation

### Data Inventory
- Maintain a data map: every system that stores personal data, by data subject type
- Include primary databases, replicas, caches, search indexes, logs, backups, third parties
- Update data inventory when new systems or processing activities are introduced

### Deletion Cascade
1. Receive and verify erasure request (identity verification)
2. Check for exceptions (legal obligation, public interest, legal claims)
3. Delete from primary data stores
4. Propagate deletion to replicas, caches, and search indexes
5. Notify third-party processors to delete (Art. 17(2))
6. Handle backup data per backup retention policy (flag for deletion at next rotation)
7. Confirm completion to data subject

### Backup Handling
- Option A: Flag records for deletion; apply deletions when backups are restored
- Option B: Encrypt individual records with per-user keys; destroy key on erasure
- Option C: Accept that backup copies will be overwritten within retention window; document this
- Document chosen approach in privacy policy and DPIA

### Confirmation
- Provide written confirmation of erasure to the data subject
- Log erasure action with timestamp and scope for audit purposes
- Retain minimal metadata about the erasure request (not the deleted data itself)

---

## Privacy by Design Principles

### 1. Proactive Not Reactive
- Anticipate privacy risks before they materialize
- Conduct privacy reviews during design phase, not after launch
- Build privacy requirements into the product backlog

### 2. Privacy as the Default
- Out-of-the-box settings must be privacy-protective
- No action required from users to protect their privacy
- Data sharing and visibility set to minimum by default

### 3. Privacy Embedded into Design
- Privacy is a core functional requirement, not an add-on
- Integrate privacy controls into the architecture (not a bolt-on layer)
- Include privacy in threat modeling and architecture reviews

### 4. Full Functionality (Positive-Sum)
- Avoid false trade-offs between privacy and functionality
- Design solutions that achieve both privacy and business objectives
- Reject "privacy vs security" as a false dichotomy

### 5. End-to-End Security (Full Lifecycle)
- Protect data from collection through deletion
- Apply security controls at every stage of the data lifecycle
- Ensure secure disposal at end of retention period

### 6. Visibility and Transparency
- Make privacy practices visible and verifiable
- Publish clear privacy policies in plain language
- Enable independent audit of privacy controls

### 7. Respect for User Privacy
- Keep the individual's interests at the center of design decisions
- Provide strong defaults, appropriate notice, and empowering options
- Design consent flows that inform rather than manipulate
