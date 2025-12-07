#!/usr/bin/env python3
"""
Simple API for Render deployment that streams updates to Vercel app
"""
import os
import sys
import json
from flask import Flask, request, Response
from core.executor_client import ExecutorClient

app = Flask(__name__)

@app.route('/')
def home():
    return {
        "message": "AI Developer & Debugger System API",
        "endpoints": {
            "health": "GET /health",
            "generate": "POST /generate"
        }
    }

@app.route('/health')
def health():
    return {'status': 'ok'}

@app.route('/generate', methods=['POST'])
def generate_code():
    """
    Generate code with streaming updates
    Expects JSON with 'requirements' field
    """
    try:
        # Get requirements from request
        data = request.get_json()
        requirements = data.get('requirements', '')
        max_iterations = data.get('max_iterations', 5)
        
        if not requirements:
            return {'error': 'No requirements provided'}, 400
        
        # Create a generator function for streaming
        def generate():
            try:
                # Initialize executor client
                client = ExecutorClient()
                
                # Run the development process and stream updates
                for update in client.run_development_process(requirements, max_iterations):
                    yield update
                    
            except Exception as e:
                error_update = {
                    "status": "error",
                    "message": f"Process error: {str(e)}",
                    "progress": 0
                }
                yield f"data: {json.dumps(error_update)}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, threaded=True)