from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)
from llama_index.llms.ollama import Ollama
import json


class SecurityWorkflow(Workflow):

    def prompt_template(self, query: str) -> str:
        query_template = f'<query> user query : {query} </query>'
        
        prompt_template = """
        You are a security layer llm your task is to determine the incoming query from user is related to given context below

        <context>

        <case>
        case 1: The given query from the user should related to creating order, viewing orders and checking order status.
        Than the response should be:

        {"permission":"granted"} 

        </case>

        <case>
        case 2: The given query from the user should be related to asking questions and doubts related to user documents.
        Than the response should be:

        {"permission":"granted"} 

        </case>

        <case>
        case 3: Any question apart from case 1 and case 2 should be denied.
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
    granted_tests = ["Can you help me place an order for the new iPhone?",
    "I'd like to check the status of my order number 12345.",
    "How do I view my past orders?",
    "Can I cancel my recent order?",
    "What are the shipping options available for my order?",
    "I have a question about the payment methods accepted for orders.",
    "Can I modify my order after it's been placed?",
    "I'm having trouble tracking my order. Can you assist me?",
    "What is the estimated delivery time for my order?",
    "I received a damaged item in my order. What should I do?"]

    denied_tests = ["What is the weather like today?",
        "Tell me a joke.",
        "Who is the current president of the United States?",
        "Can you write a poem about a cat?",
        "what is 2 + 2 in order ?",
        "Whose goverment is better?"]


    for q in granted_tests:
        print("<---------------------------->")
        print("query => ", q)
        result = await w.run(query=q)
        print("permision => ", result)
        print("<---------------------------->\n")

    print("\n<==============================>\n")

    for q in denied_tests:
        print("<---------------------------->")
        print("query => ", q)
        result = await w.run(query=q)
        print("permision => ", result)
        print("<---------------------------->\n")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
