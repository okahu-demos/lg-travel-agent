# Running and Testing via the Testing Activity Bar

## How to Run Tests for the Travel Agent Demo

1. **Set Up the Python Environment**
   - Click Ctrl+Shift+P and type in "Python: Create Environment"
   - Select Venv
   - Select Python Interpreter (Use version 3.10 to 3.13)
   - Select "Yes" when prompted "We noticed a new virtual environment has been created. Do you want to select it for the workspace folder?"

2. **Configure API Keys and Trace Export**
   - Add your `OPENAI_API_KEY` and `OKAHU_API_KEY` to a [`.env`](.env) file.
   - Set `MONOCLE_EXPORTER` in [`.env`](.env) based on where you want traces stored:
     - **Local traces only**: `MONOCLE_EXPORTER=file`
     - **Cloud traces only**: `MONOCLE_EXPORTER=okahu`
     - **Both local and cloud**: `MONOCLE_EXPORTER=file,okahu`
   - **WARNING**: You cannot manually export traces from a local environment to the Okahu Cloud

3. **Install Test Dependencies**
   ```
   cd tests
   pip install -r requirements.txt
   ```
   *Note: Tests may not appear in the Testing panel until dependencies are installed.*

4. **Start the MCP Server**
   - Open a new VS Code terminal and run `python weather-mcp-server.py` from the workspace root.
   - Keep that terminal open while tests run, then close it to stop the server when finished.

5. **Open the Testing Panel in VS Code**
   - Click the "Testing" icon in the Activity Bar (left sidebar).

6. **Run Tests**
   - Click "Run Tests" to execute all tests, or run individual test files:
     - `test_lg_travel_agent.py`
     - `test_lg_travel_agent_fluent.py`
   - View results directly in VS Code:
     - ✅ Passed tests in green
     - ❌ Failed tests in red with error details

*Note: Keep the MCP server running; the tests rely on it for weather data.*

7. **(Optional) Run Tests from Terminal**
   ```
   pytest tests/test_lg_travel_agent.py -vv
   pytest tests/test_lg_travel_agent_fluent.py -vv
   ```
   *Note: When running tests from the terminal, start the MCP server first as described in step 4 or see [README_terminal.md](README_terminal.md) step 5 for instructions on starting the mock weather MCP server.*