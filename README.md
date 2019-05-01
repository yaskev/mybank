# mybank
This is a website simulating an online bank
## Requirements
* Python 3.6
* Django 2.2
* Requests 2.21.0
## How to launch the project
* In the terminal go to the folder of the project and type ```python manage.py migrate```.
This will create (empty) database tables
* Type ```python manage.py runserver```. Now the project is available on the ```localhost``` with the specified port
## Features
* **SignUp**: Go to the ```/signup``` page on the development server. You will see the SignUp form. After you register, you will be redirected to the Login page and will be able to enter your account.
* **Login**: If you already have an account, go to ```/login``` page adn log in
* **Account management**: Click on the button ```Accounts``` in the navigation bar. On this page you can add new accounts, delete accounts and see transaction history
* **History**: One more way to see transaction history is to press ```Main``` or ```MyBank``` button and then select the desired account.
* **Transfer**: Transfer money to any other registered user to any of their accounts in any supported currency. The exchange rated are provided by ```www.exchangerate-api.com```
* **Log out**: Press this button to finish your current session and resirect you to the Login page.

## Supported entities
* **Client**: Inherits from the Django User class to support login/logout operations, as well as safe password storage
  + ```level: field to store Client's priority. The field is not used so far```
  + add_account: Create new account
  + delete_account: Delete specified account with all transactions connected with it
  + transfer: Transfer the given amount of money from one account to another by given exchange rate, create Transaction record
* **Transaction**: The model to store money movements between accounts
  + sender: Client, sender.
  + receiver: Client, receiver
  + amount_sent: Decimal, in source currency
  + amount_received: Decimal, in destination currency
  + comment: Comment provided by the sender
  + t_dttm: The datetime of the transaction
* **Account**: The model to store the current financial state of the Client
  + currency: Either RUR, USD or EUR
  + balance: Decimal
  + owner: Client
* **Admin**: ```The model of the Bank administrator. Not implemented so far.```
  + ```access_level: Integer, gives the Admin certain priviledges```
