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
                    "Book a flight from SFO to BOM on April 30th 2026. Book hotel Marriott in Central Mumbai. Also how is the weather going to be in Mumbai?")

    monocle_trace_asserter.called_tool("okahu_demo_lg_tool_book_flight","okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Mumbai").contains_input("San Francisco").contains_input("30th April 2026") \
        .contains_output("Successfully booked a flight from San Francisco to Mumbai").contains_output("success")

    monocle_trace_asserter.called_tool("okahu_demo_lg_tool_book_hotel","okahu_demo_lg_agent_lodging_assistant") \
        .contains_input("\"city\": \"Central Mumbai\",").contains_input("30th April 2026").contains_input("Marriot") \
        .contains_output("Marriot") \
        .contains_output("Central Mumbai") \
        .contains_output("success")

    monocle_trace_asserter.called_tool("demo_get_weather","okahu_demo_lg_agent_weather_assistant") \
        .contains_input("city").contains_input("Mumbai") \
        .contains_output("temperature")
    
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_weather_assistant") \
        .contains_input("Book a flight from SFO to BOM on April 30th 2026. Book hotel Marriott in Central Mumbai. Also how is the weather going to be in Mumbai?") \
        .contains_output("The weather in Mumbai") \
        .contains_output("weather") \
        .contains_output("Mumbai")

    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_lodging_assistant") \
        .contains_input("Book a flight from SFO to BOM on April 30th 2026. Book hotel Marriott in Central Mumbai. Also how is the weather going to be in Mumbai?") \
        .contains_output("Marriot at Central Mumbai") \
        .contains_output("successfully booked")
    
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Book a flight from SFO to BOM on April 30th 2026. Book hotel Marriott in Central Mumbai. Also how is the weather going to be in Mumbai?") \
        .contains_output("The flight from San Francisco to Mumbai has been successfully booked") \
        .contains_output("San Francisco to Mumbai") \
        .contains_output("successfully booked")
        
@pytest.mark.asyncio
async def test_tool_invocation(monocle_trace_asserter):

    await monocle_trace_asserter.run_agent_async(supervisor, "langgraph",
                        "Book a flight from San Francisco to Mumbai for 26th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 27th April 2026 for 4 nights.")
    
    monocle_trace_asserter.called_tool("okahu_demo_lg_tool_book_flight","okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Mumbai").contains_input("San Francisco").contains_input("26th April 2026") \
        .contains_output("Successfully booked a flight from San Francisco to Mumbai").contains_output("success")
    
    monocle_trace_asserter.called_tool("okahu_demo_lg_tool_book_hotel","okahu_demo_lg_agent_lodging_assistant") \
        .contains_input("\"city\": \"Central Mumbai\",").contains_input("27th April 2026").contains_input("Marriot Intercontinental") \
        .contains_output("Marriot Intercontinental in Mumbai").contains_output("success")

@pytest.mark.asyncio
async def test_agent_invocation(monocle_trace_asserter):
    await monocle_trace_asserter.run_agent_async(supervisor, "langgraph",
                        "Book a flight from Chennai to Bengaluru for 28th April 2026. Book a two delux rooms at ITC Hotel at Bengaluru for 29th April 2026 for 5 nights.")
    
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Book a flight from Chennai to Bengaluru for 28th April 2026. Book a two delux rooms at ITC Hotel at Bengaluru for 29th April 2026 for 5 nights.") \
        .contains_output("The flight from Chennai to Bengaluru has been successfully booked") \
        .contains_output("Chennai to Bengaluru") \
        .contains_output("successfully booked")
    
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_lodging_assistant") \
        .contains_input("Book a flight from Chennai to Bengaluru for 28th April 2026. Book a two delux rooms at ITC Hotel at Bengaluru for 29th April 2026 for 5 nights") \
        .contains_output("Your two delux rooms at ITC Hotel at Bengaluru have been successfully booked for 29th April 2026 for 5 nights.") \
        .contains_output("two delux rooms at ITC Hotel at Bengaluru") \
        .contains_output("successfully booked") \
        .contains_output("5 nights")
    
if __name__ == "__main__":
    pytest.main([__file__]) 