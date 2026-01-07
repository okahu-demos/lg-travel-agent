from asyncio import sleep
import pytest
import pytest_asyncio
from monocle_test_tools import TraceAssertion
from lg_travel_agent import setup_agents

supervisor = None

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_supervior():
    """Set up the travel booking supervisor agent."""
    global supervisor
    supervisor = await setup_agents()

@pytest.mark.asyncio
async def test_agent_and_tool_invocation(monocle_trace_asserter):
    await monocle_trace_asserter.run_agent_async(supervisor, "langgraph",
                    "Book a flight from San Francisco to Mumbai on April 30th 2026. Book hotel Marriott in Central Mumbai. Also how is the weather going to be in Mumbai?")

    monocle_trace_asserter.called_tool("okahu_demo_lg_tool_book_flight","okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Mumbai").contains_input("San Francisco") \
        .contains_output("flight").contains_output("from San Francisco to Mumbai").contains_output("booked")

    monocle_trace_asserter.called_tool("okahu_demo_lg_tool_book_hotel","okahu_demo_lg_agent_lodging_assistant") \
        .contains_input("Marriott").contains_input("Mumbai") \
        .contains_output("Marriott") \
        .contains_output("Central Mumbai") \
        .contains_output("booked")

    monocle_trace_asserter.called_tool("demo_get_weather","okahu_demo_lg_agent_weather_assistant") \
        .contains_input("city").contains_input("Mumbai") \
        .contains_output("temperature")
    
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_weather_assistant") \
        .contains_input("Book a flight from San Francisco to Mumbai on April 30th 2026. Book hotel Marriott in Central Mumbai. Also how is the weather going to be in Mumbai?") \
        .contains_output("weather") \
        .contains_output("Mumbai")

    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_lodging_assistant") \
        .contains_input("Book a flight from San Francisco to Mumbai on April 30th 2026. Book hotel Marriott in Central Mumbai. Also how is the weather going to be in Mumbai?") \
        .contains_output("Marriott") \
        .contains_output("Central Mumbai") \
        .contains_output("successfully") \
        .contains_output("booked")
    
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Book a flight from San Francisco to Mumbai on April 30th 2026. Book hotel Marriott in Central Mumbai. Also how is the weather going to be in Mumbai?") \
        .contains_output("San Francisco to Mumbai") \
        .contains_output("successfully") \
        .contains_output("booked")
        
@pytest.mark.asyncio
async def test_tool_invocation(monocle_trace_asserter):
    
    await monocle_trace_asserter.run_agent_async(supervisor, "langgraph",
                    "Book a flight from Chennai to Mumbai on April 30th 2026. Book hotel Marriott in Central Mumbai. Also how is the weather going to be in Mumbai?")

    monocle_trace_asserter.called_tool("okahu_demo_lg_tool_book_flight","okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Mumbai").contains_input("Chennai") \
        .contains_output("Successfully").contains_output("booked") \
        .contains_output("flight").contains_output("Chennai to Mumbai")
    
    monocle_trace_asserter.called_tool("okahu_demo_lg_tool_book_hotel","okahu_demo_lg_agent_lodging_assistant") \
        .contains_input("Marriott").contains_input("Mumbai") \
        .contains_output("Marriott") \
        .contains_output("Central Mumbai") \
        .contains_output("booked")

    monocle_trace_asserter.called_tool("demo_get_weather","okahu_demo_lg_agent_weather_assistant") \
        .contains_input("city").contains_input("Mumbai") \
        .contains_output("temperature")

@pytest.mark.asyncio
async def test_agent_invocation(monocle_trace_asserter):
    await monocle_trace_asserter.run_agent_async(supervisor, "langgraph",
                        "Book a flight from Chennai to Bengaluru for 28th April 2026. Book a two delux rooms at ITC Hotel at Bengaluru for 29th April 2026 for 5 nights")
    
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Book a flight from Chennai to Bengaluru for 28th April 2026. Book a two delux rooms at ITC Hotel at Bengaluru for 29th April 2026 for 5 nights") \
        .contains_output("flight") \
        .contains_output("Chennai to Bengaluru") \
        .contains_output("successfully") \
        .contains_output("booked")
    
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_lodging_assistant") \
        .contains_input("Book a flight from Chennai to Bengaluru for 28th April 2026. Book a two delux rooms at ITC Hotel at Bengaluru for 29th April 2026 for 5 nights") \
        .contains_output("ITC Hotel") \
        .contains_output("Bengaluru") \
        .contains_output("successfully") \
        .contains_output("booked")
    
if __name__ == "__main__":
    pytest.main([__file__]) 