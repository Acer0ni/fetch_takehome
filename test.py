from main import (
    create_new_user,
    spend,
    show_balance,
    transact,
    Transaction,
    process_payment,
    process_transactions,
)
import unittest


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


class Test_points(unittest.TestCase):
    async def test_proccess_transactions(self):
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
        test_list = await process_transactions(not_a_list)
        self.assertEqual(test_list, "requires list")
        test_transaction = await process_transactions(not_a_transaction)
        self.assertEqual(test_transaction, "requires transaction")
        test_process = await process_transactions(transaction_list)
        self.assertEqual(test_process, transaction_response)


if __name__ == "__main__":
    unittest.main()
