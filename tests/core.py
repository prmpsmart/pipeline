import requests, datetime
import base64, os, mimetypes


class Test:
    url_prefix = ""

    def __init__(
        self,
        url: str,
        prefix: str = "",
        access_token: str = "",
        refresh_token: str = "",
    ) -> None:
        self.prefix = prefix
        self.url = url
        self.access_token: str = access_token
        self.refresh_token: str = refresh_token

    @property
    def dt(self) -> str:
        return datetime.datetime.now()

    def log(self, log: str) -> None:
        print(f"{self.dt}::{self.prefix}{log}")

    @property
    def auth(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def path(self, path: str) -> str:
        return f"{self.url_prefix}/{path}".strip("/")

    def make_request(self, http_method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.url}/{self.path(path)}"
        self.log(f"    Test::{url}")
        try:
            response: requests.Response = requests.request(
                http_method,
                url,
                headers=self.auth,
                **kwargs,
            )

            response_json: dict = response.json()
            if user := response_json.get("user"):
                if image := user.get("image"):
                    user["image"] = len(image)

            print()
            print(response_json)
            print()

            self.access_token = response_json.get("access_token", self.access_token)
            self.refresh_token = response_json.get("refresh_token", self.refresh_token)

            self.log(
                f"        ::{url} {response.status_code} {response_json['detail']}\n"
            )
            return response_json
        except Exception as e:
            self.log(f"        ::{url} {e}\n")

    def get(self, path: str, params: dict = None) -> dict:
        return self.make_request("get", path, params=params)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.make_request("post", path, **kwargs)

    def patch(
        self, path: str, params: dict = None, json: dict = None
    ) -> requests.Response:
        return self.make_request("patch", path, params=params, json=json)

    def delete(self, path: str, params: dict = None) -> requests.Response:
        return self.make_request("delete", path, params=params)

    def to_media(self, filename: str, form: bool = False) -> dict:
        file = open(filename, "rb")
        basename = os.path.basename(filename)

        if form:
            return (basename, file, mimetypes.guess_type(filename))

        else:
            return dict(
                filename=basename,
                data=base64.b64encode(file.read()).decode(),
            )
