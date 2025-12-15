import strawberry
from typing import List
from OctoQuote.app.services.eligibility import calculate_quotes
from OctoQuote.app.services.fetch_tariffs import fetch_tariffs

@strawberry.type
class Quote:
    tariff_code: str
    annual_cost: float

@strawberry.input
class EligibilityInput:
    meter_type: str
    annual_kwh: int
    postcode: str  # unused for now

@strawberry.type
class Query:
    @strawberry.field
    def eligible_tariffs(self, input: EligibilityInput) -> List[Quote]:
        results = calculate_quotes(vars(input))
        return [Quote(**r) for r in results]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def refresh_tariffs(self, region_code: str, max_tariffs: int) -> bool:
        fetch_tariffs(region_code, max_tariffs)
        return True

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
