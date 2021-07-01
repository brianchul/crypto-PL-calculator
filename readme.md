# A crypto dex tool web
with token exchange profit & lost analyzer and dex token pair candlestick chart

support bsc network in this moment
## Demo

https://crypto-pl-calculator.herokuapp.com/

## Installaction

### to load venv to powershell, use:

```Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser```

to allow the current user to execute scripts as follows


### backend setup

``` pip install -r requirements.txt ```

### frontend setup

``` npm install ``` or see readme in ```frontend/app``` page

## Run up

### backend
``` python manager.py runserver``` 

### frontend
```npm build```
## ToDo

### backend

- [ ] support farm harvest transaction
- [ ] add transaction cache support
- [ ] add chart price cache support with mongo db
- [ ] calculate token to token ratio using graphql
- [x] fetch api add retry or rate limit
- [ ] change retry mechanism to [rate limiter](`https://gist.github.com/DannyMor/99c680c129a29b0ec315fdcaee01b6ab#file-rate_limiter-py`)
- [ ] fetch account all transaction by changing page
- [x] add log support
- [ ] write unittest
- [ ] write integration test
- [ ] support other currency mainnet
- [x] query kline support

### frontend
- [x] use table to show tokens
- [x] error handling
- [x] use funtional component
- [x] use custom hook
- [x] add button to show api data
- [ ] use chart to show P&L
- [x] token to token kline compare
- [x] add typescript support
- [ ] UI/UX
- [ ] add mvvm pattern


## license
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)