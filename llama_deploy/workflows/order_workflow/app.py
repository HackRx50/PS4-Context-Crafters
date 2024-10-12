from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
    Context,
)
from llama_index.llms.ollama import Ollama
from llama_index.utils.workflow import draw_all_possible_flows
from .agent import OrderAgent

order_agent_obj = OrderAgent()
order_agent = order_agent_obj.get_agent()

class OrderWorkflow(Workflow):
    @step
    async def step_two(self, ctx: Context, ev: StartEvent) -> StopEvent:
        
        query = f"<warning> Utilize the tools first to execute the query</warning>\n <query> {ev.query} </query>\n <instruction> Humanize the tool output and don't specify API details </instruction>"
        response = order_agent.chat(query)

        return StopEvent(result=response)


async def main():
    w = OrderWorkflow(timeout=120, verbose=True)
    # result = await w.run(query="""Create a order for product id "BAIDN31" and the product name is "TITAN watch" """)
    # result = await w.run(query=""" View all the current orders """)
    print("Enter your query:")
    query = str(input())
    result = await w.run(query=query) # """ View the status of the order with order id "7015" """

    print("Below is the output:\n\n", result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

    # draw_all_possible_flows(OrderWorkflow, filename="order_workflow.html")
