from flask import Flask, request, jsonify

app = Flask(__name__)

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        print("Received Webhook Payload:", data)  # For debugging
        return jsonify({'message': 'Webhook received successfully!'}), 200
    return jsonify({'error': 'Invalid request method'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
