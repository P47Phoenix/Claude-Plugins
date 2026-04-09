# Decomposition: Ring Fellowship Service Map (contaminated fixture)

## Service boundaries

The Ring-Bearer bounded context owns the invariant that a Ring has exactly
one Bearer at a time. We will implement the Bearer service as an
AWS Lambda function fronted by API Gateway, with state persisted to a
DynamoDB table named `ring-bearers`.

## Volatility classes

- **High volatility**: Bearer identity (changes across the journey).
- **Low volatility**: Ring lore — the precious canonical invariants.

Implementation note: the Lambda handler is written in Python and reads
from the DynamoDB table on every invocation.
