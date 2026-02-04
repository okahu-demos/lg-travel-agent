# Common Errors + Handling
Use this guide when something goes wrong while running the travel agent locally or during automated tests. Each entry lists the symptoms you may see, the most likely root cause, and the quickest recovery steps.

## 1. Pytest not found when attempting to run tests
### Result + Error Codes you may see
 * VS Code Testing pane reports "Pytest not found" and stops discovery
 * Terminal prints "ModuleNotFoundError: No module named 'pytest'"
 * This means the test cases will not run
### Likely Root Cause
 * Virtual environment not activated, so dependencies are unavailable
 * Automatic or manual installation of tests/requirements.txt failed or did not occur after cloning the repo
### Solution or Workaround
 * From the repo root: python -m venv .venv then .venv\Scripts\activate
 * Run pip install -r requirements.txt, then cd tests and pip install -r requirements.txt
 * In VS Code press Ctrl+Shift+P, select Python: Create Environment, include both requirements files, then confirm installation with pytest --version

## 2. 403 status error while exporting traces
### Result + Error Codes you may see
 * CLI logs: 403 Client Error: Forbidden for url
 * Monocle exporter reports that trace uploads failed
### Likely Root Cause
 * MONOCLE_EXPORTER includes okahu but OKAHU_API_KEY is missing or tied to a tenant without ingest permissions
 * Using an expired evaluation tenant or an API key limited to read-only access
### Solution or Workaround
 * Confirm the .env file contains a valid Okahu API key and reload the terminal session (use export or set OKAHU_API_KEY=... depending on your operating system)
 * If you only need local traces, set MONOCLE_EXPORTER=file and restart the agent
 * For cloud exports, sign in to https://portal.okahu.co, generate a fresh API key, and verify the workflow is authorized for ingestion

## 3. (Testing) ValueError during pytest run
### Result + Error Codes you may see
 * Pytest stops with ValueError: Expected ... but received ...
 * Monocle fluent assertions report that no span matched the expectation
### Likely Root Cause
 * The live model response changed and no longer matches the hard-coded expectation in tests/test_lg_travel_agent.py
 * Tests executed without deterministic mocks because the weather MCP server or environment variables were not configured
### Solution or Workaround
 * Re-run the failing prompt manually via python lg_travel_agent.py to inspect the latest answer
 * Update the expected span content in the test case or switch to the similarity-based comparisons already provided
 * When relying on mocks, ensure the weather MCP server is running so span collection completes

## 4. (Testing) Tool Not Invoked AssertionError / Context Detach Error
### Result + Error Codes you may see
 * AssertionError: Tool 'okahu_demo_lg_tool_book_flight' was never invoked by agent okahu_demo_lg_agent_air_travel_assistant with input ...
 * ERROR opentelemetry.context: Failed to detach context
 * RuntimeError: <Token used var=...> has already been used once
 * Monocle fluent assertions report: No matching operation found with given input/output criteria
 * ERROR monocle_apptrace.exporters.okahu.okahu_exporter: Traces cannot be uploaded; status code: 503, message Service Unavailable
### Likely Root Cause
 * The agent did not call the expected tool with the required input (e.g., due to prompt, logic, or model output change)
 * The test case expects a tool invocation that never occurred, or the input format does not match
 * OpenTelemetry context errors are often a side effect of failed test assertions or improper async context handling
 * Okahu Cloud was temporarily unavailable (503 Service Unavailable)
### Impact
 * Test fails and may halt further test execution
 * Trace upload to Okahu Cloud fails, but local trace is still saved
 * No impact on local agent execution, but test coverage is incomplete
 * Repeated context errors may clutter logs but do not affect core agent logic
### Solution or Workaround
 * Double-check the test input and expected tool invocation in your test case for accuracy and up-to-date prompts
 * Re-run the test and inspect the agent's actual output to see if the tool was invoked as expected
 * If the agent logic or prompt changed, update the test to match the new expected behavior
 * For context errors, ensure all async code is awaited and avoid reusing context tokens
 * If Okahu Cloud is down, retry later or use MONOCLE_EXPORTER=file to work locally
 * If you only need local traces, ignore 503 upload errors
### Additional Notes
 * This error is common when agent logic or LLM output changes, so keep tests in sync with code and prompt updates
 * If you see persistent context errors, consider updating opentelemetry and related packages to the latest version


## 5. Token limit error
### Result + Error Codes you may see
 * OpenAI API returns context_length_exceeded or the reply ends mid-sentence
 * Tests fail with truncated output and AssertionError from Monocle comparisons
### Likely Root Cause
 * MAX_OUTPUT_TOKENS environment variable is set too low (demo scenarios sometimes use 10 to simulate failures)
### Solution or Workaround
 * Remove MAX_OUTPUT_TOKENS from your environment or raise it to a safer value such as 1000
 * Shorten prompts when exploring low token stress cases

## 6. API keys not set
### Result + Error Codes you may see
 * Runtime crash: ValueError: OPENAI_API_KEY is required or KeyError: 'OPENAI_API_KEY'
 * Tests throw AssertionError: No response found in agent request span
### Likely Root Cause
 * .env file missing OPENAI_API_KEY or OKAHU_API_KEY
 * Terminal session not reloaded after editing .env
### Solution or Workaround
 * Copy .env.example to .env, add valid keys, and re-run .venv\Scripts\activate
 * Export keys in the active shell using export OPENAI_API_KEY=... and export OKAHU_API_KEY=... (use keyword '''set''' if using Windows OS)

## 7. Connection error & assertion error in testing
### Result + Error Codes you may see
 * ConnectError('All connection attempts failed') from httpx
 * Follow-on AssertionError: No response found in agent request span
### Likely Root Cause
 * Weather MCP server at http://localhost:8007/weather/mcp/ is not running when the agent fetches tools
 * Local firewall or VPN blocks requests to localhost on that port
### Solution or Workaround
 * Start the MCP server first: python weather-mcp-server.py
 * Confirm the server prints Application startup complete, then rerun the tests or agent
 * If port 8007 is occupied, set PORT=XXXX in both the server and agent environments so they match

## 8. Test telemetry folder missing or read-only
### Result + Error Codes you may see
 * Monocle exporter raises PermissionError when writing .monocle/ files
 * VS Code Okahu panel stays empty after a run
### Likely Root Cause
 * .monocle/ directory deleted or located on a drive with restrictive permissions
 * Running tests from a shell without write access to the repo folder
### Solution or Workaround
 * Recreate the folder with mkdir .monocle and ensure your user account has write permissions
 * On managed devices, move the repo to a user-writable path such as C:\Users\<you>\source\repos

## 9. Weather MCP server unavailable during tests
### Result + Error Codes you may see
 * ERROR lg_travel_agent:lg_travel_agent.py:57 Weather MCP server unavailable. Start the weather-mcp-server.py before running the agent.
 * AssertionError: No response found in agent request span
 * ValueError: Both expected and actual must be strings for sentence comparison
 * AssertionError: Tool 'okahu_demo_lg_tool_book_flight' was not invoked by agent 'None'
 * All test cases fail with similar assertion or value errors
### Likely Root Cause
 * Weather MCP server (weather-mcp-server.py) is not running on http://localhost:8007
 * Agent cannot retrieve MCP tools, causing workflow execution to fail or return None
 * Tests expect valid agent responses but receive None due to incomplete initialization
### Solution or Workaround
 * Manually start the MCP server before running tests from terminal: python weather-mcp-server.py
 * Wait for "Application startup complete" message before running pytest
 * When using VS Code Testing activity bar, the MCP server starts automatically—no manual action needed
 * Verify server is listening: curl http://localhost:8007/weather/mcp/ or check terminal output
 * If port 8007 is occupied, set PORT environment variable to match in both server and agent



# Common Warnings + Handling

These warnings do not always stop execution but are helpful early indicators of configuration drift.


## 1. Trace Export Timeout
### Result + Error Codes you may see
 * WARNING:monocle_apptrace.exporters.okahu.okahu_exporter:Trace export timed out: HTTPSConnectionPool(host='ingest.okahu.co', port=443): Read timed out. (read timeout=15)
 * Trace export timed out or failed, but local trace file is still created
### Impact
 * Local trace files are still available for debugging in VS Code
 * Cloud-based trace analysis, sharing, and evaluation will be incomplete or missing for affected runs
 * No impact on agent execution or local test results
### Likely Root Cause
 * Network connectivity issues to https://ingest.okahu.co (Okahu Cloud ingest endpoint)
 * Firewall, VPN, or proxy is blocking outbound HTTPS traffic to ingest.okahu.co
 * Okahu Cloud is experiencing downtime or maintenance
 * API key is valid but the Okahu service is slow to respond
### Solution or Workaround
 * Check your internet connection and retry after a few minutes
 * If on a corporate or restricted network, try from a different network or disable VPN/proxy
 * Confirm Okahu Cloud is operational
 * If you only need local traces, set MONOCLE_EXPORTER=file in your .env to avoid cloud export attempts
 * Note that this warning is safe to ignore if you do not require cloud trace uploads


## 2. prompt unrelated to agent purpose
 * Possible impact: The agent may refuse the task or loop between tools
 * Fix: Rephrase the prompt to focus on travel booking tasks or adjust the supervisor prompt in lg_travel_agent.py

## 3. UserWarning: MAX_OUTPUT_TOKENS set below recommended minimum
 * Possible impact: Responses truncate unexpectedly during demos
 * Fix: Increase MAX_OUTPUT_TOKENS or remove the override once your stress test is complete 
   (rt=443): Read timed out. (read timeout=15)