# Running the Demo via Terminal

## How to Run the Travel Agent Demo in the Terminal

1. **Create Python Virtual Environment**
   - Create a virtual environment:
     ```
     python -m venv .venv
     ```
2. Activate it:
     - Windows:
       ```
       .venv\Scripts\activate
       ```
     - Mac/Linux:
       ```
       . ./.venv/bin/activate
       ```

3. Configure the demo environment:

 - Mac/Linux
  
  ```
  export OKAHU_API_KEY=
  export OPENAI_API_KEY=
  ```

  - Windows
  
  ```
  set OKAHU_API_KEY=
  set OPENAI_API_KEY=
  ```

   - Set/Export `MONOCLE_EXPORTER=file,okahu` to `MONOCLE_EXPORTER=file` if you would like to have your traces only exist locally and not be exported to the cloud
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

5. **Run the Agent App**
   ```
   python lg_travel_agent.py
   ```
   or

   ```
   python lg_travel_agent_multi_turn.py
   ```
   
   > The application will prompt you for a travel booking task. It should responds with successful booking of flight and hotel, as well as weather forcast.

6. Use the following input:

   > Book a flight from SFO to BOM next week. Book a Marriott hotel in central Mumbai. Also what's the weather going to be in Mumbai next week?

   You should see a monocle generated trace in the [`.monocle`](.monocle) folder. Check out a sample trace in [`.monocle.example/monocle_trace`](.monocle.example/monocle_trace_okahu_demos_lg_travel_agent_2884cf1fe97c1a36481224157f7c6573_2026-01-09_14.59.15.json). Copy the trace file to [`.monocle`](.monocle) folder to visualize with the Okahu VS Code extension. 

   ![Run Travel Agent python](images/vscode_run_agent.png)
