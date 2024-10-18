import pexpect
from flask import Flask, jsonify
import re

app = Flask(__name__)

@app.route('/start-tailscale', methods=['POST'])
def start_tailscale():
    try:
        # Spawn the Tailscale process using pexpect
        child = pexpect.spawn('tailscale up')

        # Read the output in real-time
        auth_url = None
        while True:
            line = child.readline().decode('utf-8')  # Read one line of output at a time
            if line:
                print(f"Output: {line.strip()}")  # Print for debugging
                # Search for the URL in the output
                match = re.search(r'https?://[^\s]+', line)
                if match:
                    auth_url = match.group(0)
                    break  # Stop reading once the URL is found
            else:
                break

        # Return the URL to the client if found
        if auth_url:
            return jsonify({"auth_url": auth_url}), 200
        else:
            return jsonify({"message": "No URL found."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)
