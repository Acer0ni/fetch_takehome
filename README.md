# Install and run.

Installing this application requires Pipenv. To Install Pipenv run `pip3 install pipenv`

After cloning it down navigate to the root directory in the terminal. `pipenv sync` to download all the dependencies

`python3 main.py` to start the server

You can then use either postman or [the Fast API docs](http://localhost:8000/docs) to see it in action.

# Test

To test navigate to the applications directory and run `python3 -m unittest test.py` while making sure you are in your virtual environment.

# Use

First thing you will need to do after starting the server is make a new account. making a POST request to `/user` which will return your account id.

After that you can add transactions to the account with POST request to `transact/{accountid}`. the body must look like the following

```
{
  "payer": "string",
  "points": int,
  "timestamp": DateTime
}
```

Once you have a couple of transactions on the account you can then spend the points by making a POST to `/spend/{accountid}` with the amount of points in the body looking like this.

```
{
  "points": int
}
```

At any time you can check the balance of your transactions by making a GET request to `/balance/{accountid}` which will return a dictionary with each payers total balance.
