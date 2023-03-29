import os
from fastapi import FastAPI

from common.options import DatabaseOptions

app = FastAPI()
options = DatabaseOptions(
    host=os.environ.get('DATABASE_HOST', '127.0.0.1'),
    port=os.environ.get('DATABASE_PORT', '5432'),
    name=os.environ.get('DATABASE_NAME', 'database'),
    user=os.environ.get('DATABASE_USER', 'postgres'),
    password=os.environ.get('DATABASE_PASSWORD', 'qwerty')
)


@app.post("/graphql")
async def graphql():
    pass
