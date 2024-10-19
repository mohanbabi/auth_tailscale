from flask import Flask, request, jsonify,render_template
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



# Route to render the index.html file
@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML page


@app.route('/connect-tailscale', methods=['POST'])
def connect_tailscale():
    try:
        # Get the pre-auth key from the client's request
        data = request.json
        pre_auth_key = data.get('authkey')

        if not pre_auth_key:
            return jsonify({"error": "No auth key provided"}), 400

        # Run the Tailscale up command with the provided pre-auth key
        process = subprocess.run(['tailscale', 'up', '--authkey', pre_auth_key], capture_output=True, text=True)

        # Check if the command was successful
        if process.returncode == 0:
            return jsonify({"message": "Tailscale connected successfully!"}), 200
        else:
            return jsonify({"error": process.stderr}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)
