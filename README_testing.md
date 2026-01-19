# Running and Testing via the Testing Activity Bar

## How to Run Tests for the Travel Agent Demo

1. **Set Up the Python Environment**
   - Click Ctrl+Shift+P and type in "Python: Create Environment"
   - Select Venv
   - Select Python Interpreter (Use version 3.10 to 3.13)
   - Select "Yes" when prompted "We noticed a new virtual environment has been created. Do you want to select it for the workspace folder?"

2. **Configure API Keys**
   - Add your `OPENAI_API_KEY` and `OKAHU_API_KEY` to a `.env` file.
   - Set `MONOCLE_EXPORTER=file,okahu` to `MONOCLE_EXPORTER=file` if you would like to have your traces only exist locally and not be exported to the cloud
   - **WARNING**: You cannot manually export traces from a local environment to the Okahu Cloud  

3. **Open the Testing Panel in VS Code**
   - Click the "Testing" icon in the Activity Bar (left sidebar).

4. **Run Tests**
   - Click "Run Tests" to execute all tests, or run individual test files:
     - `test_lg_travel_agent.py`
     - `test_lg_travel_agent_fluent.py`
   - View results directly in VS Code:
     - ✅ Passed tests in green
     - ❌ Failed tests in red with error details

*Note: Test dependencies are installed automatically and the MCP server is started automatically when using the Testing activity bar.*

5. **(Optional) Run Tests from Terminal**
   ```
   pytest tests/test_lg_travel_agent.py -vv
   pytest tests/test_lg_travel_agent_fluent.py -vv
   ```
   - Note: This may require you to install dependencies manually using the following commands
   ```
   cd tests
   pip install -r requirements.txt
   ```
