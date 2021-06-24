## installaction

### to load venv to powershell, use:

```Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser```

to allow the current user to execute scripts as follows


### python setup
backend
``` pip install -r requirements.txt ```


## run up

### backend
``` python manager.py runserver```

### frontend
```npm build```
## ToDo

### backend
- [] support farm harvest transaction
- [] add transaction cache support
- [] add chart price cache support with mongo db
- [] calculate token to token ratio using graphql
- [x] fetch api add retry or rate limit
- [] change retry mechanism to rate limiter `https://gist.github.com/DannyMor/99c680c129a29b0ec315fdcaee01b6ab#file-rate_limiter-py`
- [] able to query part of transaction by using page
- [x] add log support
- [] write unittest
- [] write integration test
- [] support other currency mainnet
- [] query kline support

### frontend
- [x] use table to show tokens
- [x] error handling
- [x] use funtional component
- [x] use custom hook
- [x] add button to show api data
- [] use chart to show P&L
- [] token to token kline compare
- [x] add typescript support
- [] UI/UX
- [] add mvvm pattern