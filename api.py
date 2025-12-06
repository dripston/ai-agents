#!/usr/bin/env python3
"""
Simple API for Render deployment that streams updates to Vercel app
"""
import os
import sys
import json
import subprocess
from flask import Flask, request, Response, stream_with_context

app = Flask(__name__)

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
        
        # Create a subprocess to run the main application
        def generate_stream():
            # Send initial message
            yield f"data: {json.dumps({'status': 'started', 'message': 'Starting code generation...', 'progress': 0})}\n\n"
            
            try:
                # Run the main application as a subprocess
                process = subprocess.Popen(
                    [sys.executable, 'main.py'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )
                
                # Send requirements to the subprocess
                input_data = requirements + '\n\n' + str(max_iterations) + '\n'
                output, _ = process.communicate(input=input_data)
                
                # Process the output line by line
                for line in output.split('\n'):
                    if line.startswith('data: '):
                        yield line + '\n\n'
                    elif line.strip():
                        # For non-data lines, wrap them in our format
                        yield f"data: {json.dumps({'status': 'info', 'message': line, 'progress': 50})}\n\n"
                        
            except Exception as e:
                yield f"data: {json.dumps({'status': 'error', 'message': f'Process error: {str(e)}', 'progress': 0})}\n\n"
        
        return Response(stream_with_context(generate_stream()), mimetype='text/event-stream')
        
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, threaded=True)