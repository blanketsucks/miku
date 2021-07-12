import aiohttp
from miku.client import Client
from miku.query import Query, QueryField, QueryFields, QueryOperation
import asyncio


operation = QueryOperation(
    type="query", 
    variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
)

fields = QueryFields("Page", page="$page", perPage="$perPage")

fields.add_field("pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage")
field = fields.add_field("characters", search='$search')

field.add_field('title', 'romaji', 'man')
field.add_field('pog', 'hello', search='s')

query = Query(operation=operation, fields=fields)

print(query.build())