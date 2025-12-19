import re
from prompts import PLANNER_PROMPT, EXECUTOR_PROMPT, VERIFIER_PROMPT

MAX_RETRIES = 2


class ReasoningAgent:

    def __init__(self):  
        self.retries = 0

    # ---------- PLANNER ----------
    def planner(self, question: str) -> str:
        # In real setup → call LLM
        # Here we simulate structured planning
        plan = [
            "Parse the question",
            "Extract numbers and constrai     nts",
            "Perform calculations",
            "Validate result",
            "Format final answer"
        ]
        return "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan))

    # ---------- EXECUTOR ----------
    def executor(self, question: str, plan: str) -> dict:

        time_match = re.search(r"(\d{1,2}:\d{1,2}).*?(\d{1,2}:\d{1,2})", question)
        if time_match:
            start, end = time_match.groups()
            sh, sm = map(int, start.split(":"))
            eh, em = map(int, end.split(":"))

            if sm >= 60 or em >= 60:
                return {"result": "Invalid time format", "raw_value": None}

            start_minutes = sh * 60 + sm
            end_minutes = eh * 60 + em

            if end_minutes < start_minutes:
                end_minutes += 24 * 60

            duration = end_minutes - start_minutes
            hours, minutes = divmod(duration, 60)

            return {
                "result": f"{hours} hours {minutes} minutes",
                "raw_value": duration
            }

        return {"result": "Unable to solve", "raw_value": None}

    # ---------- VERIFIER ----------
    def verifier(self, execution_output: dict) -> dict:
        if execution_output["raw_value"] is None:
            return {
                "passed": False,
                "details": "No valid computation"
            }

        if execution_output["raw_value"] < 0:
            return {
                "passed": False,
                "details": "Negative value detected"
            }

        return {
            "passed": True,
            "details": "All checks passed"
        }

    # ---------- MAIN SOLVE ----------
    def solve(self, question: str) -> dict:
        self.retries = 0

        while self.retries <= MAX_RETRIES:
            plan = self.planner(question)
            execution = self.executor(question, plan)
            verification = self.verifier(execution)

            if verification["passed"]:
                return {
                    "answer": execution["result"],
                    "status": "success",
                    "reasoning_visible_to_user": "The problem was solved step-by-step and verified.",
                    "metadata": {
                        "plan": plan,
                        "checks": [
                            {
                                "check_name": "Basic validation",
                                "passed": True,
                                "details": verification["details"]
                            }
                        ],
                        "retries": self.retries
                    }
                }

            self.retries += 1

        return {
            "answer": "Could not determine a valid answer",
            "status": "failed",
            "reasoning_visible_to_user": "The system could not verify a correct solution.",
            "metadata": {
                "plan": plan,
                "checks": [
                    {
                        "check_name": "Basic validation",
                        "passed": False,
                        "details": "Verification failed after retries"
                    }
                ],
                "retries": self.retries
            }
        }


# ---------- CLI ----------
if __name__ == "__main__":
    agent = ReasoningAgent()
    print("Enter your question:")
    q = input("> ")
    output = agent.solve(q)
    print(output)
