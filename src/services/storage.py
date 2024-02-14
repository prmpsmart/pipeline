import firebase_admin
from firebase_admin import credentials, storage

from ..constants.config import SERVICE_ACCOUNT_JSON, FIREBASE_PROJECT_ID


def InitFirebaseApp():
    firebase_admin.initialize_app(
        credentials.Certificate(SERVICE_ACCOUNT_JSON),
        {
            "storageBucket": f"{FIREBASE_PROJECT_ID}.appspot.com",
            "databaseURL": f"https://{FIREBASE_PROJECT_ID}.firebaseio.com/",
        },
    )


def upload_media(
    filename: str,
    data: str,
    is_profile_image: bool = False,
    is_identity_image: bool = False,
    is_porfolio_image: bool = False,
) -> str:
    assert [is_profile_image, is_identity_image, is_porfolio_image].count(
        True
    ) == 1, "only one among `is_profile_image`, `is_identity_image` or `is_porfolio_image` is required"

    if is_profile_image:
        folders = "profile_images"
    elif is_identity_image:
        folders = "identity_images"
    elif is_porfolio_image:
        folders = "porfolio_images"

    destination_path = f"{folders}/{filename}"

    bucket = storage.bucket()
    blob = bucket.blob(destination_path)
    blob.upload_from_string(data)
    blob.make_public()
    download_url = blob.public_url
    return download_url


# def make_public(path: str):
#     bucket = storage.bucket()
#     blob = bucket.blob(path)
#     blob.make_public()
