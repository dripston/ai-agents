# Crew AI Developer and Debugger System

This project implements a Crew AI system with developer and debugger agents that collaborate to create, test, and deploy applications using the Meta Llama 3.1 70B model through SambaNova's API.

## Project Structure

```
.
├── agents/
│   ├── __init__.py
│   ├── developer_agent.py
│   └── debugger_agent.py
├── core/
│   ├── __init__.py
│   ├── crew.py
│   └── executor_client.py
├── api.py
├── main.py
├── stream_handler.py
├── render.yaml
├── requirements.txt
└── .env
```

## Components

### Developer Agent
- Responsible for creating code based on user requirements
- Uses the Meta Llama 3.1 70B model through SambaNova's API
- Generates clean, well-documented code following best practices

### Debugger Agent
- Reviews code created by the developer agent
- Identifies bugs, issues, and areas for improvement
- Provides detailed feedback to the developer agent
- Approves code for deployment when it meets quality standards

### Crew
- Orchestrates the collaboration between developer and debugger agents
- Manages the workflow process:
  1. Developer creates code based on requirements
  2. Debugger reviews and tests the code
  3. Feedback loop for improvements
  4. Deployment of approved code (only when explicitly approved)

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. The SambaNova API key is already included in the `.env` file

## Usage

### Command Line Interface
Run the main application:
```
python main.py
```

Then enter your development requirements when prompted. Press Enter twice to submit your requirements.

### API Interface (for Render deployment)
The system includes a Flask API for deployment on Render:
```
python api.py
```

The API exposes two endpoints:
- `GET /health` - Health check endpoint
- `POST /generate` - Code generation with streaming updates

## How It Works

1. The user provides development requirements through the terminal or API
2. The developer agent uses the Meta Llama 3.1 70B model to generate code
3. The debugger agent reviews the code for issues
4. If issues are found, feedback is sent back to the developer agent
5. This feedback loop continues until:
   - The debugger agent explicitly approves the code, OR
   - The maximum number of iterations is reached
6. Only approved code is returned as the final output

The feedback loop mechanism ensures code quality through iterative improvements:
- The debugger decides when the code is ready for deployment by explicitly stating "APPROVED"
- A maximum iteration limit prevents infinite loops
- Each iteration incorporates feedback from the previous review cycle
- Deployment only occurs when code is approved, preventing broken code from being released

## Render Deployment

This application is configured for deployment on Render with streaming updates support:

1. The `render.yaml` file contains the deployment configuration
2. The application uses Server-Sent Events (SSE) to stream real-time updates
3. Your Vercel application can connect to the `/generate` endpoint to receive continuous progress updates
4. All updates are sent in JSON format with status, message, and progress information

### Streaming Updates Format
The API streams updates in the following format:
```
data: {"status": "processing", "message": "Developer agent generating code...", "progress": 30}
```

This allows your Vercel app to provide real-time feedback to users during the code generation process.