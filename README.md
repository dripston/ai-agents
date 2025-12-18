# AI Developer & Debugger System

An AI-powered multi-agent system that automatically generates, reviews, and deploys web applications using CrewAI agents with SambaNova's LLM backend.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [System Workflow](#system-workflow)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Agents](#agents)
- [Core Components](#core-components)
- [Troubleshooting](#troubleshooting)

## Overview

This system implements an automated development workflow using two AI agents:
- **Developer Agent**: Generates production-ready HTML, CSS, and JavaScript code
- **Debugger Agent**: Reviews code quality, identifies issues, and approves deployments

The system uses a feedback loop mechanism with a maximum iteration limit to ensure code quality before deployment.

## Architecture

```
┌─────────────┐    ┌──────────────────┐    ┌──────────────┐
│             │    │                  │    │              │
│   User      │───▶│     API          │───▶│  Development │
│             │    │                  │    │    Crew      │
└─────────────┘    └──────────────────┘    └──────────────┘
                            │                       │
                            ▼                       ▼
                   ┌──────────────────┐    ┌──────────────┐
                   │                  │    │              │
                   │   Frontend       │◀───┤   Agents     │
                   │   (Vercel)       │    │              │
                   │                  │    └──────────────┘
                   └──────────────────┘
```

## System Workflow

1. **Requirements Input**: User provides development requirements via API
2. **Development Phase**: Developer agent generates code based on requirements
3. **Review Phase**: Debugger agent reviews the generated code
4. **Approval Gate**: Code must be approved (-11) or sent back for fixes (-00)
5. **Iteration**: Process repeats until approval or max iterations reached
6. **Deployment**: Approved code is prepared for deployment

## Prerequisites

- Python 3.8+
- SambaNova API key
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd coding-mas-2
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Add your SambaNova API key to the `.env` file:
```
SAMBANOVA_API_KEY=your_api_key_here
```

## Running the Application

### Local Development

Start the API server:
```bash
python api.py
```

The server will start on `http://localhost:8000` by default.

### Command Line Interface

Run the system via command line:
```bash
python main.py --cli
```

## API Endpoints

### GET /

Health check and API information endpoint.

**Response:**
```json
{
  "message": "AI Developer & Debugger System API",
  "endpoints": {
    "health": "GET /health",
    "generate": "POST /generate"
  }
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### POST /generate

Main endpoint for code generation with streaming updates.

**Request Body:**
```json
{
  "requirements": "Create a responsive website with a navigation bar and contact form",
  "max_iterations": 5
}
```

**Response:**
Server-Sent Events stream with real-time updates:
```
data: {"status": "processing", "message": "Starting development process...", "progress": 0}

data: {"status": "processing", "message": "Developer agent generating code (iteration 1)", "progress": 15}

data: {"status": "completed", "message": "Process completed successfully", "progress": 100, "result": {"html": "<!DOCTYPE html>..."}}
```

## Deployment

### Render Deployment

The application is configured for deployment on Render. The `render.yaml` file contains the deployment configuration.

1. Push your code to a GitHub repository
2. Connect your repository to Render
3. Render will automatically deploy using the configuration in `render.yaml`

### Environment Variables

Set the following environment variables in your deployment environment:
- `SAMBANOVA_API_KEY`: Your SambaNova API key

## Project Structure

```
.
├── agents/                 # AI agent implementations
│   ├── __init__.py
│   ├── developer_agent.py   # Developer agent definition
│   └── debugger_agent.py   # Debugger agent definition
├── core/                   # Core system components
│   ├── __init__.py
│   ├── crew.py             # Main crew orchestration
│   └── executor_client.py  # Client for running development process
├── api.py                  # Flask API server
├── main.py                 # Command line interface
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment configuration
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Agents

### Developer Agent

- **Role**: Senior Full-Stack Engineer
- **Model**: DeepSeek-R1-0528 via SambaNova
- **Responsibilities**: 
  - Generate production-ready HTML, CSS, and JavaScript
  - Create visually appealing, modern, interactive websites
  - Follow best practices for responsive design and accessibility

### Debugger Agent

- **Role**: Code Reviewer
- **Model**: Meta-Llama-3.3-70B-Instruct via SambaNova
- **Responsibilities**:
  - Strictly validate code quality and correctness
  - Identify bugs, security issues, and performance problems
  - Approve (-11) or reject (-00) code for deployment

## Core Components

### DevelopmentCrew (core/crew.py)

Orchestrates the development process:
- Manages agent interactions
- Implements feedback loop mechanism
- Handles iteration limits
- Provides streaming updates

### ExecutorClient (core/executor_client.py)

Client for running the development process:
- Interfaces with the DevelopmentCrew
- Handles streaming of updates
- Manages error handling

### API Server (api.py)

Flask-based API server:
- Provides REST endpoints
- Implements Server-Sent Events for streaming
- Handles CORS for cross-origin requests

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure `flask-cors` is installed and properly configured
2. **API Key Issues**: Verify your SambaNova API key is correct and active
3. **Streaming Problems**: Check network connectivity and browser compatibility

### Logs and Debugging

Enable verbose logging by setting the appropriate environment variables or modifying the agent configurations in the agent files.

### Support

For issues not covered in this README, please check the GitHub issues or contact the maintainers.