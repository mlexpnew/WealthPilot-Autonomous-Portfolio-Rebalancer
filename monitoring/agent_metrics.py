class AgentMetrics:

    def __init__(self):

        self.metrics = {}

    def record(self, agent, success=True):

        if agent not in self.metrics:

            self.metrics[agent] = {
                "runs": 0,
                "success": 0,
                "failure": 0,
            }

        self.metrics[agent]["runs"] += 1

        if success:

            self.metrics[agent]["success"] += 1

        else:

            self.metrics[agent]["failure"] += 1

    def summary(self):

        result = []

        for agent, value in self.metrics.items():

            runs = value["runs"]

            success = value["success"]

            failure = value["failure"]

            success_rate = 0

            if runs:

                success_rate = round(success * 100 / runs, 2)

            result.append({

                "agent": agent,

                "runs": runs,

                "success": success,

                "failure": failure,

                "success_rate": success_rate,

            })

        return result