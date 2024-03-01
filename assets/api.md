## Swagger UI DOCs

- [Docs](https://pipeline-mnbv.onrender.com/docs)
- [ReDoc](https://pipeline-mnbv.onrender.com/redoc)
- [Figma](https://www.figma.com/file/RRSssi71JTClhSkGwOplfv/Pipeline-Screens?type=design&node-id=0-1&mode=design)

## Auth

- /auth/register `post` ✅
  > Register a user
- /auth/login `post` ✅
  > Login a user
- /auth/forget_password `post` ✅
  > This sends a resetting link to the user's email, the email leads to the webpage's set new password page
- /auth/reset_password `post` ✅
  > Send the reset_id from the user's email and the new password to this endpoint to reset users's password
- /auth/profile `get` ✅
  > Get a user's profile
- /auth/profile `patch` ✅
  > Update a user's profile

## Pipelines

- /pipelines `get` ✅
  > Get all main pipelines
- /pipelines `post` ✅
  > Create a new main pipeline
- /pipelines/{pipeline} `get` ✅
  > Get a main pipeline
- /pipelines/{pipeline} `patch` ✅
  > Update a main pipeline
- /pipelines/{pipeline} `delete` ✅
  > Delete a main pipeline
- /pipelines/{pipeline} `post` ✅
  > Create a new branch pipeline
- /pipelines/{pipeline}/{branch} `get` ✅
  > Get a branch pipeline
- /pipelines/{pipeline}/{branch} `patch` ✅
  > Update a branch pipeline
- /pipelines/{pipeline}/{branch} `delete` ✅
  > Delete a branch pipeline

## Transactions

- /transactions `get` ✅
  > Get all transactions
- /transactions/{transaction_id} `get` ✅
  > Get a transaction
- /transactions/{pipeline} `get` ✅
  > Get a pipeline's transactions
- /transactions/{pipeline}/{branch} `get` ✅
  > Get a branch pipeline's transactions
- /transactions/send `post`
  > Send a transaction

### Paystack Webhook

- webhook `post`
