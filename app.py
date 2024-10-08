from flask import Flask, render_template, request, jsonify
import openai
import logging
import os  # Import os to use environment variables
import re  # Import re for regular expression operations

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

def extract_code(response):
    # Extract code between triple backticks
    code_blocks = re.findall(r'```[\w]*\n(.*?)```', response, re.DOTALL)
    if code_blocks:
        return '\n'.join(code_blocks)
    # If no code blocks, return the entire response
    return response.strip()

@app.route('/')
def home():
    # Renders the mermaid.html file when accessing the root URL
    return render_template('mermaid.html')

@app.route('/generate_mermaid', methods=['POST'])
def generate_mermaid():
    data = request.json
    if not data or 'description' not in data or 'apiKey' not in data:  
        missing_params = [param for param in ['description', 'apiKey'] if param not in data]
        logging.error(f"Missing required parameters: {', '.join(missing_params)}")
        print("ERROR BROKEN")
        return jsonify({'error': f"Missing required parameters: {', '.join(missing_params)}"}), 400
    
    description = data['description']
    openai.api_key = data['apiKey']

    print("descriptisssssson: ", description)
    # It's recommended to use environment variables for API keys
    # api_key = os.getenv('OPENAI_API_KEY')
    # if not api_key:
    #     logging.error("OpenAI API key is not set in environment variables.")
    #     return jsonify({'error': 'OpenAI API key is not configured on the server.'}), 500

    try:
        prompt = f"Generate Mermaid syntax for a flowchart based on the following description: {description}. Only return mermaid code starting from graph TD. DO not include mermaid in response. For example, if the description is 'A flowchart to show the process of a user signing up for a website', the response should be"
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            # api_key=api_key
        )
        mermaid_syntax = response.choices[0].message.content.strip()
        
        # Extract code block from the response
        clean_code = extract_code(mermaid_syntax)
        
        print("clean_code: ", clean_code)  # Optional: Print the cleaned code
        return jsonify({'mermaidSyntax': clean_code})  # Return the cleaned code
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'error': 'Failed to generate Mermaid syntax', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
