# DEFECT-002 Fix Notes

**Defect**: #57 -- Price Evaluator output lacks pricing source disclaimer. TC-2 showed $97 on TCGPlayer but $150+ on Card Kingdom. Users had no way to know prices were vendor-specific.

**Root Cause**: The Price Evaluator verdict and Purchase Summary used vague language ("aggregated market data", "actual costs may vary by retailer") without naming TCGPlayer as the specific source or warning about vendor price divergence.

**Fix**: v1 patch -- add explicit TCGPlayer disclaimer. Multi-source pricing is out of scope for v1.

## Files Changed

### 1. `mtg-commander/references/price-evaluator-guide.md`
- Added `PRICING_DISCLAIMER` block to the output format template (Section 4)
- Disclaimer names TCGPlayer explicitly, warns about Card Kingdom divergence, tells users to verify at their vendor

### 2. `mtg-commander/SKILL.md`
- Added `PRICING_DISCLAIMER` block to the Price Evaluator agent prompt output format
- Updated Purchase Summary Section 5: replaced vague "Pricing source: Scryfall (aggregated market data)" with "TCGPlayer market prices via Scryfall API"
- Updated Purchase Summary note: replaced generic "may vary by retailer" with explicit TCGPlayer attribution and Card Kingdom divergence warning

### 3. `mtg-commander/references/api-reference.md`
- Updated Scryfall Terms of Use section: clarified that `prices.usd` reflects TCGPlayer market price specifically, not Card Kingdom or other vendors
- Added explicit warning that Card Kingdom prices often differ significantly for staples

## Verification

- All three files compile the same message: prices are TCGPlayer via Scryfall, Card Kingdom differs, verify before buying
- Disclaimer appears in both the Price Evaluator verdict output and the final Purchase Summary -- the two places users see prices
- No behavioral changes to price fetching, budget checks, or replacement logic
- Backward compatible: no config changes, no script changes

## Not In Scope (v1)

- Multi-vendor price comparison (future enhancement)
- Card Kingdom API integration
- Price range display (low/high across vendors)
