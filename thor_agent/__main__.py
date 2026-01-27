# Agent Card

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from agent import ThorAgent

from a2a.server.request_handlers import DefaultRequestHandler
from agent_executor import ThorAgentExecutor
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.apps import A2AStarletteApplication
import uvicorn


def main(host = "localhost", port = 10004):

    skill = AgentSkill(
        id="schedule_assemble",
        name="Avengers Assemble tool",
        description="Helps with finding Thor's availability for Avengers meeting",
        tags=["scheduling", "avengers"],
        examples=["Are you free to assemble for Avengers on 2026-01-10?"]
    )

    agent_card = AgentCard(
        name="Thor's Agent",
        description="Helps with scheduling Avengers meetings",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=ThorAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=ThorAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=AgentCapabilities(),
        skills=[skill]
    )
    
    # Host the Agent
    # request handler

    request_handler = DefaultRequestHandler(
        agent_executor=ThorAgentExecutor(),
        task_store=InMemoryTaskStore(),

    )

    # host the app
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )       

    uvicorn.run(server.build(), host=host, port=port)

if __name__ == "__main__":
    main()