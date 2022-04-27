from main import (
    convert_to_dict,
    create_new_user,
    spend,
    show_balance,
    transact,
    Transaction,
    process_payment,
    process_transactions,
    app,
)
import unittest
import asyncio
from fastapi.testclient import TestClient


transaction_response = [
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
]
pay_response = [
    {"payer": "DANNON", "points": -100},
    {"payer": "UNILEVER", "points": -200},
    {"payer": "MILLER COORS", "points": -4700},
]
balance_response = {"DANNON": 1000, "UNILEVER": 0, "MILLER COORS": 5300}


class Test_points(unittest.TestCase):

    client = TestClient(app)

    def test_transactions(self):

        transaction = {
            "payer": "DANNON",
            "points": 1000,
            "timestamp": "2020-11-02T14:00:00Z",
        }
        transaction_response = [
            {
                "payer": "DANNON",
                "points": 1000,
                "timestamp": "2020-11-02T14:00:00+00:00",
            }
        ]

        account_id = Test_points.client.post("/user")

        response = Test_points.client.post(
            f"/transact/{account_id.json()}", json=transaction
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), transaction_response)

    def test_spend(self):
        account_id = Test_points.client.post("/user")
        data = {"points": 5000}
        test_list = [
            {
                "payer": "DANNON",
                "points": 1000,
                "timestamp": "2020-11-02T14:00:00Z",
            },
            {
                "payer": "UNILEVER",
                "points": 200,
                "timestamp": "2020-10-31T11:00:00Z",
            },
            {
                "payer": "DANNON",
                "points": -200,
                "timestamp": "2020-10-31T15:00:00Z",
            },
            {
                "payer": "MILLER COORS",
                "points": 10000,
                "timestamp": "2020-11-01T14:00:00Z",
            },
            {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
        ]
        test_response = [
            {"payer": "DANNON", "points": -100},
            {"payer": "UNILEVER", "points": -200},
            {"payer": "MILLER COORS", "points": -4700},
        ]

        for transaction in test_list:
            Test_points.client.post(f"/transact/{account_id.json()}", json=transaction)
        response = Test_points.client.post(f"/spend/{account_id.json()}", json=data)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_response)

    def test_proccess_transactions(self):
        self.maxDiff = None
        transaction_list = [
            Transaction(
                payer="DANNON", points=300, timestamp="2020-10-31 10:00:00+00:00"
            ),
            Transaction(
                payer="DANNON", points=-200, timestamp="2020-10-31 15:00:00+00:00"
            ),
            Transaction(
                payer="DANNON", points=1000, timestamp="2020-11-02 14:00:00+00:00"
            ),
        ]
        transaction_response = [
            Transaction(
                payer="DANNON", points=100, timestamp="2020-10-31 10:00:00+00:00"
            ),
            Transaction(
                payer="DANNON", points=1000, timestamp="2020-11-02 14:00:00+00:00"
            ),
        ]

        not_a_list = "penguins"
        not_a_transaction = [3, 9, 2, 45, 5]
        test_list = process_transactions(not_a_list)
        self.assertEqual(test_list, "requires list")
        test_transaction = process_transactions(not_a_transaction)
        self.assertEqual(test_transaction, "requires transactions")
        test_process = process_transactions(transaction_list)
        self.assertEqual(test_process, transaction_response)

    def test_process_payments(self):
        test_list = [
            Transaction(
                payer="DANNON", points=100, timestamp="2020-10-31 10:00:00+00:00"
            ),
            Transaction(
                payer="UNILEVER", points=200, timestamp="2020-10-31 11:00:00+00:00"
            ),
            Transaction(
                payer="MILLER COORS",
                points=10000,
                timestamp="2020-11-01 14:00:00+00:00",
            ),
            Transaction(
                payer="DANNON", points=1000, timestamp="2020-11-02 14:00:00+00:00"
            ),
        ]
        test_response = {
            "DANNON": {"payer": "DANNON", "points": -100},
            "UNILEVER": {"payer": "UNILEVER", "points": -100},
        }
        negative_amount = -9000
        not_a_list = "penguins"
        not_a_transaction = [3, 9, 2, 45, 5]
        # checks to make sure it rejects not a list
        requires_list = process_payment(not_a_list, 100)
        self.assertEqual(requires_list, "requires list")
        # makes sure that its a list of transactions
        test_transaction = process_payment(not_a_transaction, 100)
        self.assertEqual(test_transaction, "requires transactions")
        # checks that it rejects a negative number
        test_negative_amount = process_payment(test_list, negative_amount)
        self.assertFalse(test_negative_amount, "must be a positive amount")
        # checks to see if the amount is greater then total balance
        test_negative_balance = process_payment(test_list, 100000000)
        self.assertFalse(test_negative_balance, "amount larger then total balance")
        # makes sure the output is as expected
        test_process = process_payment(test_list, 200)
        self.assertEqual(test_process, test_response)

    def test_convert_to_dict(self):
        self.maxDiff = None
        test_list = [
            Transaction(
                payer="DANNON", points=1000, timestamp="2020-11-02 14:00:00+00:00"
            ),
            Transaction(
                payer="UNILEVER", points=200, timestamp="2020-10-31 11:00:00+00:00"
            ),
            Transaction(
                payer="DANNON", points=-200, timestamp="2020-10-31 15:00:00+00:00"
            ),
            Transaction(
                payer="MILLER COORS",
                points=10000,
                timestamp="2020-11-01 14:00:00+00:00",
            ),
            Transaction(
                payer="DANNON", points=300, timestamp="2020-10-31 10:00:00+00:00"
            ),
        ]
        response = {
            "DANNON": [
                Transaction(
                    payer="DANNON", points=1000, timestamp="2020-11-02 14:00:00+00:00"
                ),
                Transaction(
                    payer="DANNON", points=-200, timestamp="2020-10-31 15:00:00+00:00"
                ),
                Transaction(
                    payer="DANNON", points=300, timestamp="2020-10-31 10:00:00+00:00"
                ),
            ],
            "UNILEVER": [
                Transaction(
                    payer="UNILEVER", points=200, timestamp="2020-10-31 11:00:00+00:00"
                )
            ],
            "MILLER COORS": [
                Transaction(
                    payer="MILLER COORS",
                    points=10000,
                    timestamp="2020-11-01 14:00:00+00:00",
                )
            ],
        }
        test_process = convert_to_dict(test_list)
        self.assertEqual(test_process, response)


if __name__ == "__main__":
    unittest.main()
