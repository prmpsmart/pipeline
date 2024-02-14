# Models of the Fuitos App

- User

  - id `str` `unique`
  - created_timestamp `int`

  - email `str` `unique`

  - full_name `str`
  - password `str`
  - last_seen `int` `nr`
  - phone_number `str` `unique`
  - profile_image `str`
  - gender `str`
  - age `int`
  - id_verification `str`
  - id_verification_image `str`
  - location `str`
  - pin `str`
  - address `str`
  - nationality `str`

  - verifiedEmail `bool`
  - verifiedID `bool`
  - verifiedPhoneNumber `bool`

  - profession `str`
  - about `str`
  - education `str`
  - security_question `str`
  - security_answer `str`
  - job_delivery_time `int` `nr`
  - last_job_delivery `int`

  - is_artisan `bool`

- Gig

  - id `str` `unique`
  - created_timestamp `int`

  - category `str` `nr`
  - artisan_id `str`
  - description `str`
  - fee `float`
  - skills `list[str]`

- Job

  - id `str` `unique`
  - created_timestamp `int`

  - category `str`
  - client_id `str`
  - title `str`
  - description `str`
  - budget `float`
  - canceled `bool` `nr`
  - pending `bool`
  - ongoing `bool`
  - completed `bool`
  - charge_per_hour `float`

- Order

  - id `str` `unique`
  - created_timestamp `int`

  - client_id `str`
  - gig_id `str`
  - amount `float`
  - paid `bool` `nr`
  - delivery_method `str`
  - delivery_address `str`
  - delivery_phone_number `str`
  - canceled `bool`
  - pending `bool`
  - ongoing `bool`
  - completed `bool`

- Booking

  - id `str` `unique`
  - created_timestamp `int`

  - client_id `str`
  - artisan_id `str`
  - order_id `str`
  - job_id `str`
  - gig_id `str`

- Proposal

  - id `str` `unique`
  - created_timestamp `int`

  - job_id `str`
  - artisan_id `str`

- Transaction

  - id `str` `unique`
  - created_timestamp `int`

  - client_id `str`
  - isIncome `bool`
  - title `str`
  - amount `float`
  - transaction_type `str`

  - job_id `str`
  - order_id `str`

- Wallet

  - id `str` `unique`
  - created_timestamp `int`

  - user_id `str`
  - is_artisan `bool`
  - balance `float`

- Card

  - id `str` `unique`
  - created_timestamp `int`

  - card_type `str`
  - balance `float`
  - cvv `str`
  - expiry_date `str`
  - digits `str`
  - account_number `str`
  - bank `str`

- BankAccount

  - id `str` `unique`
  - created_timestamp `int`

- Message

  - id `str` `unique`
  - created_timestamp `int`

  - text `str`
  - data `str`
  - data_type `str`
  - data_size `int`

- Portfolio

  - id `str` `unique`
  - created_timestamp `int`

  - artisan_id `str`
  - description `str`
  - images `list[str]`

- Rating

  - id `str` `unique`
  - created_timestamp `int`

  - client_id `str`
  - rating `float`
  - text `str`

- InvestmentPlatform

  - id `str` `unique`
  - created_timestamp `int`

  - name `str`
  - image `str`
  - category `str`
  - roi `float`
  - price_per_unit `float`
  - percentage_fee `float`
  - still_selling `bool`

- Investment

  - id `str` `unique`
  - created_timestamp `int`

  - platform_id `str`
  - value `float`
  - fee `float`
  - phone_number `str`
  - customer_name `str`
  - units `int`
  - total `float`

- Saving

  - id `str` `unique`
  - created_timestamp `int`

- EmergencyFund

  - id `str` `unique`
  - created_timestamp `int`

- Bonus

  - id `str` `unique`
  - created_timestamp `int`

- Notification

  - id `str` `unique`
  - created_timestamp `int`

  - text `str`
  - is_artisan `bool`
  - user_id `str`
  - is_income `bool`

## Transaction Types

### Wallet based

- From Wallet
  - To Savings `wallet-savings`
  - To Investments `wallet-investments`
  - To Bank Account `wallet-bank`
- To Wallet
  - From Savings `savings-wallet`
  - From Investments `investments-wallet`
  - From Bank Account `bank-wallet`

### Savings based

- From Savings
  - To Wallet `accounted for`
  - To Investments `savings-investments`
- To Savings
  - From Wallet `accounted for`
  - From Investments `investments-savings`
