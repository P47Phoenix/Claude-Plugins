# Decomposition: Ring Fellowship Service Map (clean fixture)

## Service boundaries

The Ring-Bearer bounded context owns the invariant that a Ring has exactly
one Bearer at a time. Surrounding bounded contexts (Council, Fellowship
Roster) integrate only via domain events across the boundary.

## Volatility classes

- **High volatility**: Bearer identity (changes across the journey).
- **Low volatility**: Ring lore and canonical invariants.
- **Medium volatility**: Fellowship membership.

No implementation technology is named at this stage — only service
boundaries, bounded contexts, and volatility classes per Löwy's guidance.
