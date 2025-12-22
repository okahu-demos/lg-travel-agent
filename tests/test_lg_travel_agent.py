from asyncio import sleep
import os
import sys
import pytest 
import logging
from dotenv import load_dotenv

from lg_travel_agent import run_agent, setup_agents
from monocle_test_tools import TestCase, MonocleValidator


OKAHU_API_KEY = os.environ.get('OKAHU_API_KEY')
logging.basicConfig(level=logging.WARN)
load_dotenv()

agent_test_cases:list[TestCase] = [
    {
        "test_input": ["Book a flight from SFO to BOM on March 17th 2026."],
        "test_output": "Your flight from SFO to BOM on March 17th, 2026 has been successfully booked.",
        "comparer": "similarity",
    },
    {
        "test_input": ["Book a flight from SFO to BOM on March 17th 2026. Book hotel Marriott in Central Mumbai. Also how is the weather going to be in Mumbai?"],
        "test_spans": [
            {
                "span_type": "agentic.turn",
                # "output": "Your flight from SFO to BOM on March 17th, 2026, has been successfully booked. Additionally, your accommodation at the Marriott in Central Mumbai is confirmed. The weather in Mumbai is expected to be around 86°F. If you need further assistance, feel free to ask!",
                "comparer": "similarity",
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "okahu_demo_lg_agent_travel_supervisor"}
                ]
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "okahu_demo_lg_agent_air_travel_assistant"}
                ]
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "okahu_demo_lg_tool_book_flight"},
                    {"type": "agent", "name": "okahu_demo_lg_agent_air_travel_assistant"}
                ]
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "okahu_demo_lg_agent_lodging_assistant"}
                ]
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "okahu_demo_lg_tool_book_hotel"},
                     {"type": "agent", "name": "okahu_demo_lg_agent_lodging_assistant"}
                ]
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "okahu_demo_lg_agent_weather_assistant"}
                ]
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "demo_get_weather"},
                     {"type": "agent", "name": "okahu_demo_lg_agent_weather_assistant"}
                ]
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "okahu_demo_lg_agent_travel_supervisor"}
                ]
            }
        ]
    },
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 27th April 2026 for 4 nights.Also what is the weather going to be in Mumbai tomorrow?"],
        "test_spans": [
            {
                "span_type": "agentic.turn",
                "output": "A flight from San Francisco to Mumbai has been booked, along with a four-night stay in a two queen room at the Marriot Intercontinental in Central Mumbai, starting April 27th, 2026.",
                "comparer": "similarity",
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "okahu_demo_lg_agent_travel_supervisor"}
                ]
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "okahu_demo_lg_agent_air_travel_assistant"}
                ],
            "output": "Your flight from San Francisco to Mumbai on 26th April 2026 has been booked.",
            "comparer": "similarity"
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "okahu_demo_lg_tool_book_flight"},
                    {"type": "agent", "name": "okahu_demo_lg_agent_air_travel_assistant"}
                ],
                "output": "Flight booked from San Francisco to Mumbai.",
                "expect_errors": False,
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "okahu_demo_lg_agent_lodging_assistant"}
                ],
            "output": "Your stay at Marriot Intercontinental in Mumbai has been booked for 4 nights, starting from 27th April 2026.",
            "comparer": "similarity"
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "okahu_demo_lg_tool_book_hotel"},
                     {"type": "agent", "name": "okahu_demo_lg_agent_lodging_assistant"}
                ],
                "output": "Successfully booked a stay at Marriot Intercontinental in Mumbai.",
                "comparer": "similarity",
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "okahu_demo_lg_agent_weather_assistant"}
                ],
            "output": "The weather in Mumbai is currently",
            "comparer": "similarity"
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "demo_get_weather"},
                     {"type": "agent", "name": "okahu_demo_lg_agent_weather_assistant"}
                ],
                "output": "{\n  \"temperature\": \n}",
                "comparer": "similarity",
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "okahu_demo_lg_agent_travel_supervisor"}
                ],
            # "output": "Your flight from San Francisco (SFO) to Mumbai (BOM) on March 17th, 2026, and your stay at the Marriott in Central Mumbai have both been successfully booked. Additionally, the current weather in Mumbai is",
            "comparer": "similarity"
            }
        ]
    },
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 27th April 2026 for 4 nights."],
        "test_spans": [
            {
                "span_type": "agentic.turn",
                "output": "A flight from San Francisco to Mumbai has been booked, along with a four-night stay in a two queen room at the Marriot Intercontinental in Central Mumbai, starting April 27th, 2026.",
                "comparer": "similarity",
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "okahu_demo_lg_tool_book_flight"},
                    {"type": "agent", "name": "okahu_demo_lg_agent_air_travel_assistant"}
                ],
                "input": "{'from_airport': 'SFO', 'to_airport': 'BOM'}",
                "output": "Successfully booked a flight from SFO to BOM.",
                "expect_errors": False,
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "okahu_demo_lg_tool_book_hotel"},
                     {"type": "agent", "name": "okahu_demo_lg_agent_lodging_assistant"}
                ],
                "input": "{'hotel_name': 'Marriott Intercontinental Central Mumbai'}",
                "output": "Successfully booked a stay at Marriot Intercontinental in Central Mumbai.",
                "comparer": "similarity",
            }
        ]
    },
    
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th March 2026. Book a two queen room at Marriot Intercontinental at Juhu, Mumbai for 27th March 2026 for 4 nights."],
        "test_spans": [
            {
            "span_type": "agentic.turn",
            "eval":
                {
                "eval": "bert_score",
                "args" : [
                    "input", "output"
                ],
                "expected_result": {"Precision": 0.5, "Recall": 0.5, "F1": 0.5},
                "comparer": "metric"
                }
            }
        ]
    },
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th March 2026."],
        "mock_tools": [
            {
                "name": "okahu_demo_lg_tool_book_flight",
                "type": "tool.adk",
                "response": {
                    "status": "success",
                    "message": "Flight booked from {{from_airport}} to {{to_airport}}."
                }
            }
        ],
        "test_spans": [
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "okahu_demo_lg_tool_book_flight"} 
                ],
                "output": "Successfully booked a flight from San Francisco to Mumbai",
                "comparer": "similarity",
            }
        ]
    },
]

@MonocleValidator().monocle_testcase(agent_test_cases)
async def test_run_agents(my_test_case: TestCase):
    await MonocleValidator().test_workflow_async(run_agent, my_test_case)
    # coordinator = await setup_agents()
    # await MonocleValidator().test_agent_async(coordinator, "langgraph", my_test_case)
    await sleep(2) # Ensure all telemetry is flushed

if __name__ == "__main__":
    pytest.main([__file__]) 