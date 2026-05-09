# Output Contract: test-data

The `test-data` task type produces a test data specification. Sub-agent output must match this template:

```
## Test Data Specification: [FEATURE/SCENARIO NAME]

### Data Requirements
| Entity | Fields | Valid Values | Invalid Values | Edge Cases |
|---|---|---|---|---|

### Data Sets
| Set Name | Purpose | Record Count | Notes |
|---|---|---|---|

### Setup / Teardown
[How data is created, loaded, and cleaned up]

### Data Dependencies
[Relationships between entities, ordering constraints]
```
