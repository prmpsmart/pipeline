from src.utils.commons import get_timestamp
from tests import *

url = "https://pipeline-mnbv.onrender.com"
url = "http://127.0.0.1:8000"

email = "miracle.apata@mailinator.com"
password = "securepassword123"

auth = AuthTest(url)

# auth.register(
#     full_name="Miracle Apata",
#     email=email,
#     phone_number="+2348168524477",
#     password=password,
#     # image='',
# )

auth.login(
    email=email,
    password=password,
)

# auth.forgot_password(email)
# auth.reset_password(427893, email, "new_password")


pipeline = PipelineTest(url)
pipeline.access_token = auth.access_token

pipelines = ["P1", "P2", "P3"]
pi = 0

# pipeline.get_pipelines()

# pipelines
# pipeline.create_pipeline(pipelines[pi+1], 5)
pipeline.get_pipeline(pipelines[pi])
# pipeline.update_pipeline(pipelines[pi], 900)
pipeline.delete_pipeline(pipelines[pi])


branches = ["B1", "B2", "B3"]
bi = 0
# branches
pipeline.create_branch(pipelines[pi], branches[bi], 40)
# pipeline.get_branch(pipelines[pi], branches[bi])
# pipeline.update_branch(pipelines[pi], branches[bi], 30)
# pipeline.delete_branch(pipelines[pi], branches[bi])
