from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)
from llama_index.llms.ollama import Ollama
from llama_index.utils.workflow import draw_all_possible_flows
import json


class SecurityWorkflow(Workflow):

    def prompt_template(self, query: str) -> str:
        query_template = f'<query> user query : {query} </query>'
        
        prompt_template = """
        You are a security layer llm your task is to determine the incoming query from user is related to given context below

        <context>

        <case>
        case 1:  The given query from the user should related to creating a order using product name, viewing orders using Order Id and order status using order Id .
        Than the response should be:

        {"permission":"granted"} 

        </case>

        <case>
        case 2: The given query from the user also can be related to retriving user documents using document id.
        Than the response should be:

        {"permission":"granted"} 

        </case>

        <case>
        case 3: If the user tries to query about recommendations or opinions permission should be denied.
        Than the response should be:

        {"permission":"denied"} 

        </case>

        </context>

        """ 

        prompt = prompt_template + query_template
        
        return prompt

    @step
    async def step_one(self, ev: StartEvent) -> StopEvent:
        llm = Ollama(model="gemma2:2b", request_timeout=60.0, temperature=0.1, json_mode=True)

        prompt = self.prompt_template(ev.query)

        response = llm.complete(prompt)
        check = json.loads(response.text)

        return StopEvent(result=str(check["permission"]))


async def main():
    w = SecurityWorkflow(timeout=60, verbose=False)
    result = await w.run(query="what is the order?")
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

    # draw_all_possible_flows(SecurityWorkflow, filename="security_layer_workflow.html")