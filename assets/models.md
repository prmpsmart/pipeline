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
  - deleted `bool`

- Transaction

  - id `str` `unique`
  - created_timestamp `int`

  - type `str`
  - amount `float`
  - status `str`

  - from_main_pipeline `str` `nr`
  - from_branch_pipeline `str`

  - to_main_pipeline `str`
  - to_branch_pipeline `str`

  - sender `str`
  - sender_id `str`
  - sender_bank `str`

  - receiver `str`
  - receiver_id `str`
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
  - percentage `float`
  - deleted `bool` `nr`
  - deleted_timestamp `int` `nr`

- BranchPipeline

  - id `str` `unique`
  - created_timestamp `int`

  - name `str`
  - main_pipeline `str`
  - email `str`
  - percentage `float`
  - deleted `bool` `nr`
  - deleted_timestamp `int` `nr`
