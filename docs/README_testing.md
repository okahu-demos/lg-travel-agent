# Run tests in VS Code to QA agents locally

This demo includes examples of trace-driven tests that are reproducible even for agents that rely on LLMs to make QA on agents easy. These tests rely on `monocle-test-tools` package that add AI abstraction on top of `pytest`. 

Monocle provides: 
- Native integration for pytest compatible tools including VS Code
- Automatic trace capture during test execution for easy debugging of failed tests 
- Validation of agent and tool invocations
- Fluent assertions based on GenAI abstractions
- Management of tests and traces in the cloud for observability 


## Run Tests via Testing Panel

1. **Configure API keys and Trace Export**
   - Configure these settings in the [`.env`](../.env) file by following the [prerequisites](../README.md#prerequisites).
   - **WARNING**: You cannot manually export traces from a local environment to the Okahu Cloud

2. **Set Up the Python Environment**
   - Click Ctrl+Shift+P and type in "Python: Create Environment"
   - Select Venv
   - Select Python Interpreter (Use version 3.10 to 3.13)
   - Select the following as dependencies to install requirements.txt and tests/requirements.txt
      - Manually install dependencies via [terminal](#run-tests-via-terminal) if you are not prompted for dependencies or are facing issues with this step
   - Select "Yes" if prompted "We noticed a new virtual environment has been created. Do you want to select it for the workspace folder?"
   
   *Note: Tests may not appear in the Testing panel until dependencies are installed.*

3. **Open the Testing Panel in VS Code**
   - Click the "Testing" icon in the Activity Bar (left sidebar).

   ![Testing in VS Code](../images/testing_vs_code_icon.png)

4. **Run Tests**
   - Click the "Run Tests" button to execute all tests or run individual test files:
      - [`test_lg_travel_agent.py`](../tests/test_lg_travel_agent.py) - Using assertions on any span property in monocle generated traces. 
      - [`test_lg_travel_agent_fluent.py`](../tests/test_lg_travel_agent_fluent.py) - Using fluent assertions such as `called_tool()`, `called_agent()`, `contains_input()`


5. **Review results directly inside VS Code:**
   - ✅ Passed tests appear in green
   - ❌ Failed tests surface detailed error messages alongside trace links

   ![Passed and failed test cases](../images/vscode_tests.png)

*Note: The MCP server is started automatically when using the Testing activity bar.*

## Run Tests via Terminal
1. **Install Python Dependencies**
   ```
   cd tests
   pip install -r requirements.txt
   ```

2. **Start the Weather MCP Server**
      - From the workspace root, run `python weather-mcp-server.py`
      - Wait for the "Application startup complete" log message before executing pytest
      - For alternative startup options, check out [README_terminal.md](README_terminal.md#L33-L71) step 5 for instructions

3. **Alternatively, execute targeted suites from the terminal:**
      ```bash
      pytest tests/test_lg_travel_agent.py -vv
      ```
      or
      ```bash
      pytest tests/test_lg_travel_agent_fluent.py -vv
      ```