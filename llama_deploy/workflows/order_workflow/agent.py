from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from .agent_tool import (
    create_order_tool,
    view_orders_tool,
    order_status_tool,
)
from .agent_template import api_agent_prompt

class OrderAgent:
    def __init__(self) -> None:

        # agent tools
        _create_order_tool = FunctionTool.from_defaults(fn=create_order_tool)
        _view_orders_tool = FunctionTool.from_defaults(fn=view_orders_tool)
        _order_status_tool = FunctionTool.from_defaults(fn=order_status_tool)

        # llm
        _llm = Ollama(model="gemma2:2b", request_timeout=60.0)

        # list of tools
        _tools = [_create_order_tool, _view_orders_tool, _order_status_tool]

        # initializing ReAct agent
        self.agent = ReActAgent.from_tools(tools=_tools, llm=_llm, verbose=True)

        # replacing system prompt for ReAct agent
        self.agent.update_prompts({"agent_worker:system_prompt": api_agent_prompt})

    def get_agent(self):
        return self.agent