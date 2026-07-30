from asyncio import sleep
import pytest
import pytest_asyncio
from monocle_test_tools import TraceAssertion
from lg_travel_agent_multi_turn_v2 import setup_agents, generate_session_id

supervisor = None
session_id = None

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_supervior():
    """Set up the travel booking supervisor agent."""
    global supervisor
    supervisor = await setup_agents()
    global session_id
    if session_id is None:
        session_id = generate_session_id()


@pytest.mark.asyncio
@pytest.mark.repeat(3)  # Repeat the test 3 times to check for consistency
async def test_flight_and_hotel_booking(monocle_trace_asserter):

    await monocle_trace_asserter.run_agent_async(supervisor, "langgraph", "Book a flight from Chennai for 28th August 2026", session_id=session_id)
    await monocle_trace_asserter.run_agent_async(supervisor, "langgraph", "Bengaluru", session_id=session_id)
    await monocle_trace_asserter.run_agent_async(supervisor, "langgraph", "Book a hotel Marriott in Bengaluru", session_id=session_id)

    # Turn 1: Agent asks for destination (no tool call)
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Book a flight from Chennai for 28th August 2026") \
        .does_not_call_tool("okahu_demo_lg_tool_book_flight","okahu_demo_lg_agent_air_travel_assistant") \
        .contains_any_output("please","specify", "provide", "destination", "city", "arrival")

    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_air_travel_assistant") \
        .does_not_call_tool("okahu_demo_lg_tool_book_flight")

    # Turn 2: Agent books flight with complete info
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Bengaluru") \
        .contains_output("flight") \
        .contains_output("Chennai to Bengaluru") \
        .contains_output("successfully") \
        .contains_output("booked")
    
    monocle_trace_asserter.called_tool("okahu_demo_lg_tool_book_flight","okahu_demo_lg_agent_air_travel_assistant") \
        .contains_input("Chennai") \
        .contains_input("Bengaluru") \
        .contains_output("Successfully booked a flight from Chennai to Bengaluru") 

    monocle_trace_asserter \
        .called_agent("okahu_demo_lg_agent_air_travel_assistant") \
        .under_token_limit(500) \
        .under_duration(3, units="seconds", span_type="agent_invocation")

    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_lodging_assistant") \
            .contains_input("Book a hotel Marriott in Bengaluru") \
            .contains_output("Marriott") \
            .contains_output("Bengaluru") \
            .contains_any_output("successfully", "booked")

    monocle_trace_asserter.called_tool("okahu_demo_lg_tool_book_hotel","okahu_demo_lg_agent_lodging_assistant") \
            .contains_input("hotel_name") \
            .contains_input("Marriott") \
            .contains_output("booked")

    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_air_travel_assistant", count=2)
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_travel_supervisor", count=6)
    monocle_trace_asserter.called_agent("okahu_demo_lg_agent_lodging_assistant", count=1)

@pytest.mark.asyncio
async def test_eval_on_flight_and_hotel_booking_session(monocle_trace_asserter):
    monocle_trace_asserter \
        .with_trace_source("okahu", id=session_id, fact_name="session", workflow_name="okahu_demos_lg_travel_agent_tests") \
        .with_evaluation("okahu") \
        .check_eval("frustration",
                    fact_name="agentic_sessions",
                    expected="frustrated") \
        .check_eval("hallucination",
                    fact_name="agentic_sessions",
                    expected="major_hallucination")
    
if __name__ == "__main__":
    pytest.main([__file__])
