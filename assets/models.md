# Models of the Fuitos App

- User

  - id `str`
  - created_timestamp `int`

  - full_name `str`
  - email `str`

  - password `str`
  - phone_number `str` `nr`
  - profile_image `str`

- Transaction

  - id `str` `unique`
  - created_timestamp `int`

  - amount `float` `nr`
  - sender `str`
  - receiver `str`
  - main_pipeline `str`
  - branch_pipeline `str`
  - remark `str`
  - originating_bank `str`

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
