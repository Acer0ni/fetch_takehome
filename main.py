from datetime import datetime
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
        Transaction(payer="Alice", points=400, timestamp="2017-01-01T00:00:03Z"),
        Transaction(payer="Alice", points=-200, timestamp="2019-01-01T00:00:03Z"),
        Transaction(payer="Bob", points=200, timestamp="2018-01-02T00:00:00Z"),
        Transaction(payer="Bob", points=-100, timestamp="2018-01-02T00:00:00Z"),
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
    return e.timestamp


async def process_transactions(transaction_list):

    for transaction in transaction_list:
        if transaction.points < 0:
            amount = abs(transaction.points)
            x = 0
            while amount > 0:
                if x > len(transaction_list) - 1:
                    break
                elif transaction_list[x].points < 0:
                    x += 1
                    continue
                elif transaction_list[x].points > amount:
                    transaction_list[x].points -= amount
                    amount = 0
                elif amount >= transaction_list[x].points:
                    amount -= transaction_list[x].points
                    del transaction_list[x]
                    print(transaction_list)
                    x = 0
                else:
                    x += 1
            transaction_list.remove(transaction)
    return transaction_list


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
        payer_dict[payer] = await process_transactions(payer_dict[payer])
    processed_list = payer_dict.values()
    print(processed_list)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
    )


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
