from .core import Test


class JobTest(Test):
    url_prefix = "jobs"

    def all(self):
        return self.get("")

    def new(
        self,
        category: str,
        title: str,
        description: str,
        budget: float,
        charge_per_hour: float,
    ):
        return self.post(
            "new",
            json=dict(
                category=category,
                title=title,
                description=description,
                budget=budget,
                charge_per_hour=charge_per_hour,
            ),
        )
