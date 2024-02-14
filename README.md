# Fuitos App REST backend server.

## Details

### Figma

[12/7/2023 12:05 AM] Favour West: https://www.figma.com/file/v3cXY3To7v4hZzmuG6iAJ1/FUITOS-BETA-APP?type=design&node-id=0%3A1&mode=design&t=nRJ5J485GVRtrBYo-1

### Gmail

- [12/7/2023 12:05 AM] Favour West: Fuitosapp@gmail.com
- [12/7/2023 12:07 AM] Favour West: #Fu1tos@pp

## Endpoints

### Artisan Sequence

#### Auth

- /artisans/register

  - method: `POST`
  - request payload:

    ```py
    full_name: str
    email: str
    phone_number: str
    password: str
    profession: str
    about: str
    education: str
    profile_image: str
    age: int
    id_verification: str
    id_verification_image: str
    ```

- /artisans/forgot_password

  - method: `POST`
  - request payload:

    ```py
    email: str
    ```

- /artisans/reset_password

  - method: `POST`
  - request payload:

    ```py
    otp: int
    email: str
    password: str
    ```

- /artisans/login

  - method: `POST`
  - request payload:

    ```py
    email_or_username: str
    password: str
    ```

#### Home

- /artisans/jobs

  - method: `GET`
  - header: `Authentication Bearer {token}`
  - request parameters:

    ```py
    popular: bool
    ```

  - response data:

    ```py
    jobs: list[dict]=[{
        job_title: str
        charge_per_hour: float
        job_types: list[str]
        description: dict = {
            text: str,
            bullets: list[str]
        }
    }]
    ```

- /artisans/jobs/search

  - method: `POST`
  - header: `Authentication Bearer {token}`
  - request payload:

    ```py
    category: str
    sub_category: str
    location: str
    min_salary: float
    max_salary: float
    job_types: list[str] = [full_time, part_time, freelancer, remote, contract]
    ```

  - response data:

    ```py
    jobs: list[dict]=[{
        job_title: str
        charge_per_hour: float
        job_types: list[str]
        description: dict = {
            text: str,
            bullets: list[str]
        }
    }]
    ```

#### User

- /artisans/profile

  - method: `GET`
  - header: `Authentication Bearer {token}`
  - response data:

    ```py
    id: str
    name: str
    email: str
    date_of_birth: str
    gender: str
    ```

- /artisans/change_password

  - method: `POST`
  - header: `Authentication Bearer {token}`
  - request payload:

    ```py
    password: str
    sign_out_other_devices: bool
    ```

- /artisans/update_portfolio

  - method: `POST`
  - header: `Authentication Bearer {token}`
  - request payload:

    ```py
    previous_works: list[dict] = [{
        image: str,
        description: str,
        }]
    work_description: dict = {
        title: str = 'Painter',
        size: str,
        location: str,
        min_price: float,
        max_price: float,
    }
    location: str # lat, log selected from the map on the device.
    ```

- /artisans/rating

  - method: `GET`
  - header: `Authentication Bearer {token}`
  - response data:

    ```py
    rating: float = 3.71
    stars: dict[str, int] = {
        one: int = 0
        two: int = 2
        three: int = 1
        four: int = 1
        five: int = 3
    }
    reviews: list[dict[str, Any]] = [{
        client_name: str
        star: int
        comment: str
        timestamp: int
    }]
    ```

- /artisans/earnings

  - method: `GET`
  - header: `Authentication Bearer {token}`
  - response data:

    ```py
    income_history: list[dict[str, Any]] = [{
        title: str
        amount: float
        timestamp: int
    }]
    ```

### Artisan Wallet Sequence

### Artisan Investment sSequence

### Client Sequence

#### Auth

- /clients/register

  - method: `POST`
  - request payload:

    ```py
    full_name: str
    email: str
    password: str
    address: str
    nationality: str
    gender: str
    id_verification_image: str
    age: int
    id_verification: str
    ```

- /clients/forgot_password

  - method: `POST`
  - request payload:

    ```py
    email: str
    ```

- /clients/reset_password

  - method: `POST`
  - request payload:

    ```py
    otp: int
    password: str
    ```

- /clients/login

  - method: `POST`
  - request payload:

    ```py
    email_or_username: str
    password: str
    ```

#### Home

- /clients/artisans/category

  - method: `POST`
  - request payload:

    ```py
    categories: list[dict] = [{
        name: str
        active_jobs: int
    }]
    ```

- /clients/jobs

  - method: `GET`
  - header: `Authentication Bearer {token}`
  - response data:

    ```py
    jobs: list[dict[str, Any]] = [{
        title: str
        amount: float
        timestamp: int
        status: str = ['ongoing', 'cancelled', 'pending']
    }]
    ```

- /clients/artisans/search

  - method: `POST`
  - header: `Authentication Bearer {token}`
  - request payload:

    ```py
    category: str
    sub_category: str
    location: str
    min_salary: float
    max_salary: float
    job_types: list[str] = [full_time, part_time, freelancer, remote, contract]
    ```

  - response data:

    ```py
    jobs: list[dict]=[{
        job_title: str
        charge_per_hour: float
        job_types: list[str]
        last_seen: int
        job_delivery_time: int
        last_job_delivery: int
        description: dict = {
            text: str,
            bullets: list[str]
        }
    }]
    ```

- /clients/artisans/trending

  - method: `GET`
  - header: `Authentication Bearer {token}`
  - response data:

    ```py
    jobs: list[dict]=[{
        job_title: str
        charge_per_hour: float
        job_types: list[str]
        last_seen: int
        job_delivery_time: int
        last_job_delivery: int
        description: dict = {
            text: str,
            bullets: list[str]
        }
    }]
    ```

- /clients/artisans/close_by

  - method: `POST`
  - header: `Authentication Bearer {token}`
  - request payload:
    ```py
    longitude: float
    latitude: float
    ```
  - response data:

    ```py
    jobs: list[dict]=[{
        job_title: str
        charge_per_hour: float
        job_types: list[str]
        last_seen: int
        job_delivery_time: int
        last_job_delivery: int
        description: dict = {
            text: str,
            bullets: list[str]
        }
    }]
    ```

#### User

- /clients/profile

  - method: `GET`
  - header: `Authentication Bearer {token}`
  - response data:

    ```py
    id: str
    name: str
    email: str
    date_of_birth: str
    gender: str
    ```

- clients/proposals

  - method: `GET`
  - header: `Authentication Bearer {token}`
  - response data:

    ```py
    proposals: list[dict[str, Any]] = [{
        artisan_id: str
        artisan_name: str
        message: str
        timestamp: int
    }]
    ```

- clients/delete_account

  - method: `DELETE`
  - header: `Authentication Bearer {token}`

- clients/logout

  - method: `GET`
  - header: `Authentication Bearer {token}`

### Admin Sequence

- admin/dashboard

  - method: `GET`
  - header: `Authentication Bearer {token}`
  - response data:

    ```py
    artisans: list[dict[str, Any]] = [{
        artisan_id: str
        artisan_name: str
        image: str
        category: str
        price: float
        instagram: str
        facebook: str
        be: str
    }]
    ```

- admin/artisans

  - method: `GET`
  - header: `Authentication Bearer {token}`
  - response data:

    ```py
    artisans: list[dict[str, Any]] = [{
        artisan_id: str
        artisan_name: str
        image: str
        category: str
        price: float
        instagram: str
        facebook: str
        be: str
    }]
    ```
