# Models of the Pipeline App

- SessionDb

  - id `str`
  - created_timestamp `int`

  - user_id `str`
  - deleted_timestamp `int` `nr`

- User

  - id `str`
  - created_timestamp `int`

  - full_name `str`
  - email `str`

  - password `str`
  - phone_number `str` `nr`
  - image `str`
  - verified `bool` `nr`

- Transaction

  - id `str` `unique`
  - created_timestamp `int`

  - type `str`
  - amount `float` `nr`
  - status `str`

  - main_pipeline `str`
  - branch_pipeline `str`

  - sender `str`
  - sender_bank `str`

  - receiver `str`
  - receiver_bank `str`

  - account_no `str`

  - remark `str`
  - session_id `str`

- Wallet

  - id `str` `unique`
  - created_timestamp `int`

  - email `str`
  - balance `float`

- MainPipeline

  - id `str` `unique`
  - created_timestamp `int`

  - name `str`
  - email `str`
  - balance `float`

- BranchPipeline

  - id `str` `unique`
  - created_timestamp `int`

  - name `str`
  - main_pipeline `str`
  - email `str`
  - balance `float`
