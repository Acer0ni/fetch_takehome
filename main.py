from datetime import datetime
from os import times
from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()


class Transaction(BaseModel):
    payer: str
    points: int
    timestamp: datetime


accounts = {
    0: [
        Transaction(payer="Alice", points=100, timestamp="2016-01-01T00:00:03Z"),
        Transaction(payer="Alice", points=200, timestamp="2022-01-01T00:00:03Z"),
        Transaction(payer="Alice", points=400, timestamp="2019-01-01T00:00:03Z"),
        Transaction(payer="Bob", points=200, timestamp="2018-01-02T00:00:00Z"),
        Transaction(payer="sean", points=300, timestamp="2022-01-02T00:00:02Z"),
    ]
}


@app.post("/transact/{account_id}", status_code=201)
async def transact(account_id: int, transactions: list[Transaction]):
    if account_id not in accounts:
        print("id not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=account_id)
    accounts[account_id].extend(transactions)


@app.post("/show/{account_id}")
async def show(account_id: int):
    return accounts[account_id]


def myFunc(e):
    print(e.timestamp)
    return e.timestamp


@app.post("/spend/{account_id}")
async def spend(account_id: int, amount: int):
    if account_id not in accounts:
        print("id not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=account_id)
    account = accounts[account_id]
    payer_dict = {}
    for transaction in account:
        if transaction.payer not in payer_dict:
            payer_dict[transaction.payer] = [transaction]
        else:
            payer_dict[transaction.payer].append(transaction)
    for payer in payer_dict:
        payer_dict[payer].sort(key=myFunc)

    return payer_dict


# process each payer,remove negatives and when a transaction is empty remove it from temp list
# ???
# look at each payer to see if value is negative
# take from the oldest transaction, remove if empty
# put the remaining transactions in a list sorted by date
# start "emptying" transactions, adding a new transaction to the account when i take points from a payer,
# as transactions happen set up a return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
