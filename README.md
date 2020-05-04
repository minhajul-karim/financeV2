# Finance v2.0

## Goal
Build a web application where users can check the stock prices listed in IEX, buy & sell shares and check their transaction history.

## Basic features
1. Registration.
2. Login.
3. Portfolio of shares.
4. View quote of stocks.
5. Buy shares.
6. Sell shares.
7. View transaction history.

## Additional features
1. Form validation.
2. Check for any existing account while registration.
3. Reset password.
4. Buy & sell shares right from the portfolio.

*These additional features added complexity to the application which led to the following issues.*

## Issues
1. The code became huge and had to maintain.
2. The form validation required a couple of external JS files which increased the load time.
3. Writing queries and managing the database was difficult.

## Solution
To standardize this application the following steps were taken:
1. The application factory and blueprints made this app modular and easy to maintain.
2. Flask-WTF increased the security, made the form validation easier, & most importantly kicked out the additional form validation scripts.
3. ORM using Flask-SQLAlchemy made the database interactions neat and readable.







