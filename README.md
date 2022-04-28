# Install and Run

Installing this application requires Pipenv. To Install Pipenv run `pip3 install pipenv`

Clone the repo, then navigate to its root directory in a terminal.

`pipenv sync` to download all the dependencies.

`python3 main.py` to start the server.

You can then use either postman or [the Fast API docs](http://localhost:8000/docs) to see it in action.

# Test

For testing, navigate to the application directory in terminal, then run `python3 -m unittest test.py`

You must be in a virtual environment.

# Use

Step one after starting the server is to make a new user account.

Making a POST request to `/user` will create the user and return your account id.

After that you can add transactions to the account with a POST request to `transact/{accountid}`. The body must use the following format:

```
{
  "payer": "string",
  "points": int,
  "timestamp": DateTime
}
```

Once you have multiple transactions on the account you can then spend the points by making a POST request to `/spend/{accountid}`. Be sure to specify the amount of points using the following format:

```
{
  "points": int
}
```

At any time you can check the balance of your transactions by making a GET request to `/balance/{accountid}`

This will return a dictionary with each payer's total balance.
