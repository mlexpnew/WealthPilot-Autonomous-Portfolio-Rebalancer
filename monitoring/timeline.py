from datetime import datetime


class ExecutionTimeline:

    def start(self):

        return {
            "started_at": datetime.now().isoformat(),
            "steps": [],
        }

    def log(self, timeline, agent, message):

        timeline["steps"].append({

            "time": datetime.now().strftime("%H:%M:%S"),

            "agent": agent,

            "message": message,

        })

    def finish(self, timeline):

        timeline["finished_at"] = datetime.now().isoformat()

        return timeline