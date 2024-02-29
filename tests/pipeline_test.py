from .core import Test


class PipelineTest(Test):
    url_prefix = "pipelines"

    def get_pipelines(self):
        return self.get("")

    def create_pipeline(self, name: str, percentage: float):
        return self.post(
            "",
            json=dict(
                name=name,
                percentage=percentage,
            ),
        )

    def get_pipeline(self, pipeline: str):
        return self.get(pipeline)

    def update_pipeline(self, pipeline: str, percentage: float):
        return self.patch(
            pipeline,
            json=dict(
                percentage=percentage,
            ),
        )

    def delete_pipeline(self, pipeline: str):
        return self.delete(pipeline)

    def create_branch(self, pipeline: str, name: str, percentage: float):
        return self.post(
            pipeline,
            json=dict(
                name=name,
                percentage=percentage,
            ),
        )

    def get_branch(self, pipeline: str, branch: str):
        return self.get(f"{pipeline}/{branch}")

    def update_branch(self, pipeline: str, branch: str, percentage: float):
        return self.patch(
            f"{pipeline}/{branch}",
            json=dict(
                percentage=percentage,
            ),
        )

    def delete_branch(self, pipeline: str, branch: str):
        return self.delete(f"{pipeline}/{branch}")
