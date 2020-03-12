# Project goal
*This project is an enhancement of Finance, a CS50X assignment. The task was to build a web application where users can check the stock prices listed in IEX, buy & sell shares and check their transaction history. I took the project a bit further and implemented features such as,*

* Form validation.
* Check for any existing account while registration.
* Reset password.
* Buy & sell shares right from the portfolio.

*These features added complexity to the application which led to the following issues:*
1. The code became huge and had to maintain.
2. The form validation required a couple of external JS files which increased the load time.
3. Writing queries and managing the database was difficult.

*Solution*
To standardize this application the following steps were taken:
1. The application factory and blueprints made this app modular and easy to maintain.
2. Flask-WTF increased the security, made the form validation easier, & most importantly kicked out the additional form validation scripts.
3. ORM using Flask-SQLAlchemy made the database interactions neat and readable.


*Other Features:*
1. Registration.
2. Login.
3. Portfolio of shares.
4. View quote of stocks.
5. Buy shares.
6. Sell shares.
7. View transaction history.




