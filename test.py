from main import create_new_user, spend, show_balance, transact
import asyncio


new_transactions = [
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
    {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
    {"payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z"},
    {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
]
transaction_response = [
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
    {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
    {"payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z"},
    {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
]
pay_response = [
    {"payer": "DANNON", "points": -100},
    {"payer": "UNILEVER", "points": -200},
    {"payer": "MILLER COORS", "points": -4700},
]
balance_response = {"DANNON": 1000, "UNILEVER": 0, "MILLER COORS": 5300}


async def main():
    account_id = await create_new_user()
    assert await transact(account_id, new_transactions) == transaction_response
    print(await spend(account_id, 5000))
    assert await show_balance(account_id) == balance_response


if __name__ == "__main__":
    asyncio.run(main())
