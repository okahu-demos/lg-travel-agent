# Running the Demo with the "Run" Button (Top Right)

## How to Run the Travel Agent Demo Using the "Run" Button

1. **Create Python Virtual Environment**
   - Click Ctrl+Shift+P and type in "Python: Create Environment"
   - Select Venv
   - Select Python Interpreter (Use version 3.10 to 3.13)
   - Select "Yes" when prompted "We noticed a new virtual environment has been created. Do you want to select it for the workspace folder?"

2. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

3. **Configure API Keys and Trace Export**
   - Add your `OPENAI_API_KEY` and `OKAHU_API_KEY` to a [`.env`](.env) file.
   - Set `MONOCLE_EXPORTER` in [`.env`](.env) based on where you want traces stored:
     - **Local traces only**: `MONOCLE_EXPORTER=file`
     - **Cloud traces only**: `MONOCLE_EXPORTER=okahu`
     - **Both local and cloud**: `MONOCLE_EXPORTER=file,okahu`
   - **WARNING**: You cannot manually export traces from a local environment to the Okahu Cloud    

4. **Start the mock weather MCP server**    
  - Mac/Linux
  
  ```
  python weather-mcp-server.py > mcp.out 2>&1 & while ! grep -q "Application startup complete" mcp.out; do sleep 0.2; done; grep "Application startup complete" mcp.out
  ```

  - Windows Command Prompt(CMD)
  
  ```
  cmd /c "start "" /B cmd /c ^"python -u weather-mcp-server.py > mcp.out 2>&1^" & :wait & powershell -Command ^"Start-Sleep -Milliseconds 2000^" 
  findstr /C:^"Application startup complete^" mcp.out"
  ```

  - Windows Powershell(pwsh)
  
  ```
  Start-Process -FilePath powershell -ArgumentList '-NoProfile','-Command','python weather-mcp-server.py *> ''mcp.out''' -WindowStyle Hidden 
  Select-String -Path mcp.out -Pattern 'Application startup complete' -AllMatches | ForEach-Object { $_.Matches.Value }
  ```

  **Expected output**: `Application startup complete`

  > This application is a travel agent app that mocks travel-related tasks such as flight booking, hotel booking, and checking weather in a city.  
  > It is a Python program using the LangGraph agent framework.  
  > The app uses the OpenAI gpt-4o model for inference.

5. **Open a file in VS Code**
   - Open `lg_travel_agent.py` or `lg_travel_agent_multi_turn.py`
   - Click the "Run" button (▶) in the top right corner of the editor window.

6. **Interact with the App**
   - The app will start in the integrated terminal.
   
   > The application will prompt you for a travel booking task. It should responds with successful booking of flight and hotel, as well as weather forcast.

7. Use the following input:

   > Book a flight from SFO to BOM next week. Book a Marriott hotel in central Mumbai. Also what's the weather going to be in Mumbai next week?

   You should see a monocle generated trace in the [`.monocle`](.monocle) folder. Check out a sample trace in [`.monocle.example/monocle_trace`](.monocle.example/monocle_trace_okahu_demos_lg_travel_agent_2884cf1fe97c1a36481224157f7c6573_2026-01-09_14.59.15.json). Copy the trace file to [`.monocle`](.monocle) folder to visualize with the Okahu VS Code extension. 

   ![Run Travel Agent python](images/vscode_run_agent.png)