# OctoQuote

OctoQuote is a small Python backend service that exposes energy tariff eligibility and pricing logic via a GraphQL API.

---

## What the service does

- Fetches real electricity tariff data from the Octopus Energy public API
- Normalises and freezes tariff data as configuration
- Exposes a GraphQL API to:
  - Determine tariff eligibility based on customer inputs
  - Calculate estimated annual energy costs
- Allows controlled refresh of tariffs by region and count via a GraphQL mutation

---