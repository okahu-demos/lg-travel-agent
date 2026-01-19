import subprocess
import sys
from pathlib import Path
import asyncio
import os
import time
from dotenv import load_dotenv
from typing import Any, Optional
from uuid import UUID
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph_supervisor import create_supervisor
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph.state import CompiledStateGraph

# Load environment variables from .env file
load_dotenv()
OKAHU_API_KEY = os.getenv("OKAHU_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Automatically install requirements.txt if needed
def ensure_requirements_installed():
    req_file = Path(__file__).parent / "requirements.txt"
    if req_file.exists():
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(req_file)
        ], check=True)

ensure_requirements_installed()

# Enable Monocle Tracing
from monocle_apptrace import setup_monocle_telemetry
setup_monocle_telemetry(workflow_name = 'okahu_demos_lg_travel_agent', monocle_exporters_list = 'file,okahu')

import logging
logger = logging.getLogger(__name__)
DEFAULT_PORT = 8007
port = int(os.getenv("PORT", DEFAULT_PORT))

# Global max output tokens (can be overridden via environment variable MAX_OUTPUT_TOKENS)
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "1000"))

def model_factory():
    """Create a ChatOpenAI model instance with the global max token setting."""
    return ChatOpenAI(model="gpt-4o", max_tokens=MAX_OUTPUT_TOKENS)

@tool("okahu_demo_lg_tool_book_hotel", description="Book a hotel for a stay")
def book_hotel(hotel_name: str):
    """Book a hotel"""
    return f"Successfully booked a stay at {hotel_name}."

@tool("okahu_demo_lg_tool_book_flight", description="Book a flight from one airport to another")
def book_flight(from_airport: str, to_airport: str):
    """Book a flight"""
    return f"Successfully booked a flight from {from_airport} to {to_airport}."

# Set up MCP client for monocle repo
async def get_mcp_tools():
    """Get tools from the monocle MCP server."""
    client = MultiServerMCPClient(
        {
            "weather": {
                "url": f"http://localhost:{port}/weather/mcp/",
                "transport": "streamable_http",
            }
        }
    )
    # get list of all tools from the MCP server and their descriptions
    tools = await client.get_tools()
    return tools

# Set up agents for travel booking
async def setup_agents():

    weather_tools = await get_mcp_tools()

    flight_assistant = create_agent(
    model=model_factory(),
        tools=[book_flight],
        system_prompt="You are a flight booking assistant. You only handle flight booking. Just handle that part from what the user says, ignore other parts of the requests.",
        name="okahu_demo_lg_agent_air_travel_assistant"
    )

    hotel_assistant = create_agent(
    model=model_factory(),
        tools=[book_hotel],
        system_prompt="You are a hotel booking assistant. You only handle hotel booking. Book hotel if the user explicitly asks, just handle that part from what the user says, ignore other parts of the requests.",
        name="okahu_demo_lg_agent_lodging_assistant"
    )

    weather_agent = create_agent(
    model=model_factory(),
        tools=weather_tools,
        system_prompt="You are a weather information assistant. Please use the tool available to you for checking weather. Extract city name from the user query and pass it to the weather tool, and ignore other parts of the requests.",
        name="okahu_demo_lg_agent_weather_assistant"
    )
    supervisor = create_supervisor(
        supervisor_name="okahu_demo_lg_agent_travel_supervisor",
        agents=[flight_assistant, hotel_assistant, weather_agent],
    model=model_factory(),
        prompt=(
            "You manage a hotel booking assistant and a"
            "flight booking assistant. Assign work to them. Each assistant is skilled in their own area ONLY and cannot do other tasks. "
            "If the user asks for weather information, delegate to the weather assistant."
        )
    ).compile()

    return supervisor



# Run the agent with a user request
async def run_agent_turn(supervisor, request: str, session_id: str):
    config: Optional[dict[str, Any]] = {
        "configurable": {
            "thread_id": session_id
        }
    }
    chunk = await supervisor.ainvoke(
        input={
            "messages": [
                {
                    "role": "user",
                    "content": request
                }
            ]
        }, config=config
    )
    return chunk

# Run the agent with a user request
async def run_agent_session(session_id: str):
    supervisor: CompiledStateGraph = await setup_agents()

    while True:
        try:
            request: str = input("\nI am a travel booking agent. How can I assist you with your travel plans? (You can ask me to book flights, hotels, or check the weather at any location.): ")
        except EOFError:
            print("\nBye...")
            break
        chunk = await run_agent_turn(supervisor, request, session_id)
        print(chunk["messages"][-1].content)

def generate_session_id() -> str:
    return str(UUID(int=time.time_ns()))  # Simple UUID based on current time

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    asyncio.run(run_agent_session(generate_session_id()))