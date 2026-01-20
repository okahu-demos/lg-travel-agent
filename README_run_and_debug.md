# Running the Demo with "Run and Debug"

## How to Run the Travel Agent Demo Using "Run and Debug"

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

*Note: The MCP server is started automatically in this mode*

3. **(Optional) Open the Project in VS Code**
   - Open `lg_travel_agent.py` or `lg_travel_agent_multi_turn.py`

    > This application is a travel agent app that mocks travel-related tasks such as flight booking, hotel booking, and checking weather in a city.  
    > It is a Python program using the LangGraph agent framework.  
    > The app uses the OpenAI gpt-4o model for inference.

4. **Start "Run and Debug"
   - Click the "Run and Debug" icon in the Activity Bar (left sidebar).
   - Select 
        - `Python Debugger: lg-travel-agent Single Turn`, 
        - `Python Debugger: lg-travel-agent Multi Turn`, 
        - OR `Python: Current File` if you have the current file open
   - Click the green "Run and Debug" button.

5. **Use the App**
   - The app will run in debug mode, allowing you to set breakpoints and inspect variables.
   
   > The application will prompt you for a travel booking task. It should responds with successful booking of flight and hotel, as well as weather forcast.

6. Use the following input:

   > Book a flight from SFO to BOM next week. Book a Marriott hotel in central Mumbai. Also what's the weather going to be in Mumbai next week?

   You should see a monocle generated trace in the [`.monocle`](.monocle) folder. Check out a sample trace in [`.monocle.example/monocle_trace`](.monocle.example/monocle_trace_okahu_demos_lg_travel_agent_2884cf1fe97c1a36481224157f7c6573_2026-01-09_14.59.15.json). Copy the trace file to [`.monocle`](.monocle) folder to visualize with the Okahu VS Code extension. 

   ![Run Travel Agent python](images/vscode_run_agent.png)
