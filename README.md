### **CRDC Datahub Submission Agent**

This project develops a custom AI agent to automate the approval process of CRDC Datahub submission requests using a Federal Lead account. Built with Python and Playwright for browser automation, this agent locates pending submissions, evaluates their content, and approves them by simulating actions taken by a Federal Lead reviewer.

Designed for seamless execution in QA environments, the agent supports remote deployment and leverages CrewAI for modular orchestration. Operating independently from the submission agent, it focuses on the review and approval stage of the submission lifecycle. Optional integration with vector databases allows for decision logging and refinement via AI feedback loops.


## Setup
1. **Activate the Python virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

2. **Add Login Info to .env file**
```
   TOTP_SECRET=YOUR_TOTP_SECRET
   LOGIN_USERNAME=YOUR_LOGIN_USERNAME
   LOGIN_PASSWORD=YOUR_LOGIN_PASSWORD
```

3. **Install requirements**
   ```bash
   pip install boto3 pyotp playwright
   ```

4. To run, cd into the main folder, and run

```bash
PYTHONPATH=src python src/fedlead_agent_crewai/main.py   
```    
