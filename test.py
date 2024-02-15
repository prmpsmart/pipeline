from src.utils.commons import get_timestamp
from tests import *

url = "https://pipeline-mnbv.onrender.com"
url = "http://127.0.0.1:8000"

artisan_email = "miracle.apata@mailinator.com"
artisan_password = "securepassword123"

auth = AuthTest(url)

# auth.register_artisan(
#     full_name="Miracle Apata",
#     email=artisan_email,
#     phone_number="+2348168524477",
#     password=artisan_password,
#     profession="Backend Developer",
#     about="I am a dedicated backend developer with expertise in Python, Dart, TypeScript, and JavaScript. I thrive in collaborative environments, contributing to the development of efficient and scalable software solutions.",
#     education="B.Eng in Electrical and Electronics Engineering, Federal University of Technology, Akure",
#     profile_image="https://example.com/miracle_apata_profile.jpg",
#     age=26,
#     id_verification="Verified",
#     id_verification_image="https://example.com/miracle_apata_id_card.jpg",
# )


client_email = "john.doe@mailinator.com"
client_password = "secure_password123"
client_password = "new_password"

# auth.register_client(
#     full_name="John Doe",
#     email=client_email,
#     password=client_password,
#     address="123 Main Street, Cityville, State",
#     nationality="US",
#     gender="male",
#     id_verification_image="https://example.com/miracle_apata_profile.jpg",
#     age=25,
#     id_verification="verified",
# )

artisan = 0

if artisan:
    auth.login(
        email_or_username=artisan_email,
        password=artisan_password,
    )
else:
    auth.login(
        email_or_username=client_email,
        password=client_password,
    )

# auth.forgot_password(client_email)
# auth.reset_password(427893, client_email, "new_password")

job = JobTest(url, access_token=auth.access_token)

# job.new(
#     category="Web Development",
#     title="Build a responsive website",
#     description="Build a responsive website for a small business using HTML, CSS, and JavaScript.",
#     budget=1500.00,
#     charge_per_hour=50.00,
# )
job.all()
