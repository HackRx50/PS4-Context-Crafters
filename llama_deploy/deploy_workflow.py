from llama_deploy import (
    deploy_workflow,
    WorkflowServiceConfig,
    ControlPlaneConfig,
)
import asyncio
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step
from workflows.order_workflow.app import OrderWorkflow
from workflows.security_workflow.app import SecurityWorkflow

async def main():
    security_task = asyncio.create_task(
        deploy_workflow(
            SecurityWorkflow(),
            WorkflowServiceConfig(
                host="127.0.0.1", port=8011, service_name="security_layer_agent"
            ),
            ControlPlaneConfig(),
        )
    )

    order_task = asyncio.create_task(
        deploy_workflow(
            OrderWorkflow(),
            WorkflowServiceConfig(
                host="127.0.0.1", port=8012, service_name="order_agent"
            ),
            ControlPlaneConfig(),
        )
    )

    await asyncio.gather(security_task, order_task)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())