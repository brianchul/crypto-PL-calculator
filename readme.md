## installaction

### to load venv to powershell, use:

```Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser```

to allow the current user to execute scripts as follows


### python setup
backend
``` pip install -r requirements.txt ```


## run up

### backend
``` flask run --port APP_PORT```


## ToDo

### backend
[] support farm harvest transaction
[x] add retry or rate limit to prevent ddos
[] change retry mechanism to rate limiter `https://gist.github.com/DannyMor/99c680c129a29b0ec315fdcaee01b6ab#file-rate_limiter-py`
[] able to query part of transaction by using page
[x] add log support
[] write unittest
[] write integration test
[] able to use other currency
[] query kline support

### frontend
[] use table to show tokens
[] use chart to show P&L
[] token to token kline compare
