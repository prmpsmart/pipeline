from .core import Test


class AuthTest(Test):
    url_prefix = "auth"

    def register_artisan(
        self,
        full_name: str,
        email: str,
        phone_number: str,
        password: str,
        profession: str,
        about: str,
        education: str,
        profile_image: str,
        age: int,
        id_verification: str,
        id_verification_image: str,
    ):
        return self.post(
            "register_artisan",
            json=dict(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                password=password,
                profession=profession,
                about=about,
                education=education,
                profile_image=profile_image,
                age=age,
                id_verification=id_verification,
                id_verification_image=id_verification_image,
            ),
        )

    def register_client(
        self,
        full_name: str,
        email: str,
        password: str,
        address: str,
        nationality: str,
        gender: str,
        id_verification_image: str,
        age: int,
        id_verification: str,
    ):
        return self.post(
            "register_client",
            json=dict(
                full_name=full_name,
                email=email,
                password=password,
                address=address,
                nationality=nationality,
                gender=gender,
                id_verification_image=id_verification_image,
                age=age,
                id_verification=id_verification,
            ),
        )

    def login(self, email_or_username: str, password: str):
        return self.post(
            "login",
            json=dict(
                email_or_username=email_or_username,
                password=password,
            ),
        )

    # def send_otp(self):
    #     return self.get("send_otp")

    # def verify_otp(self, otp: int):
    #     return self.post(
    #         "verify_otp",
    #         json=dict(
    #             otp=otp,
    #         ),
    #     )

    def forgot_password(self, email: str):
        return self.post(
            "forgot_password",
            json=dict(
                email=email,
            ),
        )

    # def verify_reset_otp(self, otp: int, email: str):
    #     return self.post(
    #         "verify_reset_otp",
    #         json=dict(
    #             otp=otp,
    #             email=email,
    #         ),
    #     )

    def reset_password(self, otp: int, email: str, password: str):
        return self.post(
            "reset_password",
            json=dict(
                otp=otp,
                email=email,
                password=password,
            ),
        )

    # def delete_users(self, unique_id: str):
    #     return self.post(
    #         "delete_users",
    #         json=dict(
    #             unique_id=unique_id,
    #         ),
    #     )
