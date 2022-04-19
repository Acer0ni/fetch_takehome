from xmlrpc.client import DateTime
from fastapi import FastAPI, status
from pydantic import BaseModel
from requests import Response
from fastapi.responses import JSONResponse

app = FastAPI()


class Transaction(BaseModel):
    payer: str
    points: int
    timestamp: DateTime


accounts = {
    0: [
        Transaction(payer="Alice", points=100, timestamp="2020-01-01T00:00:00Z"),
        Transaction(payer="Bob", points=200, timestamp="2020-01-02T00:00:00Z"),
    ]
}


@app.post("/transact/{account_id}", status_code="201")
async def transact(account_id: int, transactions: list[Transaction]):
    if account_id not in accounts:
        print("id not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=account_id)
    accounts[account_id].extend(transactions)


@app.post("spend/{account_id}")
async def spend(account_id: int, amount: int):
    if account_id not in accounts:
        print("id not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=account_id)
    account = accounts[account_id]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
