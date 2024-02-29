from .core import Test


class AuthTest(Test):
    url_prefix = "auth"

    def register(
        self,
        full_name: str,
        email: str,
        phone_number: str,
        password: str,
        image: str = "",
    ):
        return self.post(
            "register",
            json=dict(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                password=password,
                image=image,
            ),
        )

    def login(self, email: str, password: str):
        return self.post(
            "login",
            json=dict(
                email=email,
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

    def get_profile(self):
        return self.get("profile")

    def update_profile(
        self,
        full_name: str = "",
        email: str = "",
        phone_number: str = "",
        image: str = "",
    ):
        return self.patch(
            "profile",
            json=dict(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                image=image,
            ),
        )
