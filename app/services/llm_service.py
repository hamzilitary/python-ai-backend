import httpx
import time
from app.db.connection import get_connection
from app.db.quireies import get_run, complete_run, update_status, fail_run, claim_run
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3"

class RunNotFoundError(ValueError):
    pass
class InvalidStatusError(ValueError):
    pass

class LLLService:
    def __init__(self):
        self.model = ChatOllama(model="gemma3")
        

    def do_work(self, goal: str, context: str | None):
        if "fail" in goal:
            raise RuntimeError("Goal can not contain the word fail")
        if context is None:
            context = ""

        messages = [SystemMessage(content= "You are an AI assistant responsible for completing the user's goal"),
                     HumanMessage(content=f"Goal: {goal}\nContext: {context}")]
        
        response = self.model.invoke(messages)
        return response.content

    def execute_run(self, run_id: int):
        claimed = claim_run(
            run_id
        )
        if claimed is None:
            run = get_run(
                run_id
            )
            if run is None:
                raise RunNotFoundError("ID must exists to execute run")
            print(run)

            if run.status != "pending":
                raise InvalidStatusError(f"Status is not pending, ,unable to exucute run for id: {run_id}")
            

        goal_process = claimed.goal

        try:
            response_output = self.do_work(goal_process, claimed.context)
        except RuntimeError as e:
            print("Goal can not contain the word fail")
            error_update_status = fail_run(
                run_id,
                str(e)
            )
            print(error_update_status)
            raise 

        complete_run_rresult = complete_run(
            run_id,
            response_output
        )
        print(complete_run_rresult)
        return complete_run_rresult


        

