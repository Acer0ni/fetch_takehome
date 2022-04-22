import copy
from datetime import datetime, timezone
from urllib import response
from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()


class Transaction(BaseModel):
    payer: str
    points: int
    timestamp: datetime


accounts = {}


def myFunc(e):
    return e.timestamp


async def process_transactions(transaction_list: list):

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
                else:
                    x += 1
            transaction_list.remove(transaction)
    return transaction_list


async def flatten_dict(processed_dict: dict):
    flat_list = []
    for payer in processed_dict:
        for transaction in processed_dict[payer]:
            flat_list.append(transaction)
    return flat_list


async def process_payment(transaction_list: list, amount: int):
    response_dict = {}
    for transaction in transaction_list:
        if amount == 0:
            break
        if amount <= transaction.points:
            if transaction.payer not in response_dict:
                response_dict[transaction.payer] = {
                    "payer": transaction.payer,
                    "points": amount * -1,
                }
            else:
                response_dict[transaction.payer]["points"] -= amount
            amount = 0
        else:

            amount -= transaction.points
            if transaction.payer not in response_dict:
                response_dict[transaction.payer] = {
                    "payer": transaction.payer,
                    "points": transaction.points * -1,
                }
            else:
                response_dict[transaction.payer]["points"] -= transaction.points
    if amount != 0:
        return False
    return response_dict


async def convert_to_dict(account):
    payer_dict = {}
    for transaction in account:
        if transaction.payer not in payer_dict:
            payer_dict[transaction.payer] = [transaction]
        else:
            payer_dict[transaction.payer].append(transaction)
    return payer_dict


async def tally_transactions(payer_dict, response_dict):
    for payer in payer_dict:
        for transaction in payer_dict[payer]:
            response_dict[payer] += transaction.points
    return response_dict


@app.post("/user")
async def create_new_user():
    account_id = len(accounts)
    accounts[account_id] = []
    return account_id


@app.post("/transact/{account_id}", status_code=201)
async def transact(account_id: int, transactions: list[Transaction]):
    if account_id not in accounts:
        print("id not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=account_id)
    accounts[account_id].extend(transactions)
    return accounts[account_id]


@app.get("/show/{account_id}")
async def show(account_id: int):
    return accounts[account_id]


@app.post("/spend/{account_id}")
async def spend(account_id: int, points: int):
    if account_id not in accounts:
        print("id not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=account_id)
    account = copy.deepcopy(accounts[account_id])
    payer_dict = await convert_to_dict(account)
    for payer in payer_dict:
        payer_dict[payer].sort(key=myFunc)
        payer_dict[payer] = await process_transactions(payer_dict[payer])
    processed_list = await flatten_dict(payer_dict)
    processed_list.sort(key=myFunc)
    response_dict = await process_payment(processed_list, points)

    if not response_dict:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="not enough points"
        )
    response_string = []
    for payer in response_dict:
        new_transaction = Transaction(
            payer=response_dict[payer]["payer"],
            points=response_dict[payer]["points"],
            timestamp=datetime.now(tz=timezone.utc),
        )
        accounts[account_id].append(new_transaction)
        transaction_string = {
            "payer": response_dict[payer]["payer"],
            "points": response_dict[payer]["points"],
        }
        response_string.append(transaction_string)

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_string)


@app.get("/balance/{account_id}")
async def show_balance(account_id: int):
    if account_id not in accounts:
        print("id not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=account_id)
    account = copy.deepcopy(accounts[account_id])
    payer_dict = await convert_to_dict(account)
    response_dict = {}
    for payer in payer_dict:
        response_dict[payer] = 0
        payer_dict[payer].sort(key=myFunc)
        payer_dict[payer] = await process_transactions(payer_dict[payer])
    response_dict = await tally_transactions(payer_dict, response_dict)
    return response_dict


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
