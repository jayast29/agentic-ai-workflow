import asyncio
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver

from tools import get_availability

# Load environment variables
load_dotenv()

# Initialize memory
memory = MemorySaver()

class ThorAgent:
    """Thor's scheduling assistant agent."""
    
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]
    
    def __init__(self):
        """Initialize the ThorAgent with model, tools, and system prompt."""
        self.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.tools = [get_availability] if get_availability else []
        self.system_prompt = (
            "You are Thor's scheduling assistant.\n"
            "Your job is to use the 'get_availability' tool "
            "to answer questions about Thor's schedule for Avengers assemble.\n\n"
            "If the question is unrelated to scheduling, politely say you can't help.\n"
        )
        self.graph = create_agent(
            self.model,
            tools=self.tools,
            system_prompt=self.system_prompt,
            checkpointer=memory
        )
    
    async def get_response(self, query: str, context_id: int) -> dict:

        inputs = {"messages": [("user", query)]}
        config = {"configurable": {"thread_id": context_id}}
        
        raw_response = self.graph.invoke(inputs, config)
        messages = raw_response.get("messages", [])
        
        ai_messages = [
            message.content 
            for message in messages 
            if isinstance(message, AIMessage)
        ]
        
        if not ai_messages:
            return {"content": "No response"}
        
        # Handle both string content and list of content parts
        content = ai_messages[-1]
        if isinstance(content, list):
            # Extract text from content parts
            text_parts = [
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in content
            ]
            response = " ".join(text_parts)
        else:
            response = str(content)
        
        return {"content": response}
    