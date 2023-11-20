from main.query_processing import process_query
from flask import Flask, request, jsonify
from firebase_admin import auth
from functools import wraps

app = Flask(__name__)

def authenticate_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            id_token = request.headers.get('Authorization')
            decoded_token = auth.verify_id_token(id_token)
            request.user_id = decoded_token['uid']

            return f(*args, **kwargs)
        except auth.AuthError:
            return jsonify({'error': 'Unauthorized'}), 401

    return decorated_function


@app.route('/question', methods=['POST'])
@authenticate_request
def ask_question():
    user_id = request.user_id

    data = request.get_json()
    question = data['question']

    reply, document_path = process_query(question, "federal")

    return jsonify({
        "document_path": document_path,
        "reply": reply
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
