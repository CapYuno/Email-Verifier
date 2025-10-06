from flask import Flask, render_template, request, jsonify
from email_verifier import EmailVerifier

app = Flask(__name__)
verifier = EmailVerifier()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    email = request.form.get('email', '')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    results = verifier.verify_email(email)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)