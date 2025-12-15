from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from OctoQuote.app.schema import schema

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
