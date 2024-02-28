## Auth

- /auth/login `post`
  > login a user
- /auth/register `post`
  > register a user
- /auth/forget_password `post`
  > this sends a resetting link to the user's email, the email leads to the webpage's set new password page
- /auth/reset_password `post`
  > send the reset_id from the user's email and the new password to this endpoint to reset users's password

## Pipelines

- /pipelines `get`

  > get all pipelines

- /pipelines/{pipeline_id} `post`
  > creating a new pipeline
- /pipelines/{pipeline_id} `patch`
  > updating a single pipeline

## Transactions

- /transactions `get`
  > get all transactions
- /transactions/{transaction_id} `get`
  > get a single transaction
