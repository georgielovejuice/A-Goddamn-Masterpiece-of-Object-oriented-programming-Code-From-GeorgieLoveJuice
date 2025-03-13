from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/main')  # This is the main page where the chatbot will be
def main():
    return render_template('main.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get("message")
    return jsonify({"reply": user_message})  # Echoes back the user message

if __name__ == '__main__':
    app.run(debug=True)
