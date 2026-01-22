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

4. **Open the Testing Panel in VS Code**
   - Click the "Testing" icon in the Activity Bar (left sidebar).

5. **Run Tests**
   - Click "Run Tests" to execute all tests, or run individual test files:
     - `test_lg_travel_agent.py`
     - `test_lg_travel_agent_fluent.py`
   - View results directly in VS Code:
     - ✅ Passed tests in green
     - ❌ Failed tests in red with error details

*Note: The MCP server is started automatically when using the Testing activity bar.*

6. **(Optional) Run Tests from Terminal**
   ```
   pytest tests/test_lg_travel_agent.py -vv
   pytest tests/test_lg_travel_agent_fluent.py -vv
   ```
   *Note: When running tests from the terminal, you must manually start the MCP server first. See [README_terminal.md](README_terminal.md) step 5 for instructions on starting the mock weather MCP server.*