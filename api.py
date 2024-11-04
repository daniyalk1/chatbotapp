from flask import Flask, request, jsonify, send_from_directory
from app import generate_response_with_rag
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__, static_folder="./chatbot_ui")

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("user_input")
    if not user_input:
        return jsonify({"error": "No input provided"})

    response = generate_response_with_rag(user_input)
    return jsonify({"response": response})

@app.route('/test', methods=['GET'])
def test():
    return "Welcome to the National Foods Chatbot API!"

#react apps route handler
@app.route('/', defaults={'path1': '', 'path2': '','path3': ''})
@app.route('/<path:path1>', defaults={'path2': '','path3': ''})
@app.route('/<path:path1>/<path:path2>',defaults={'path3': ''})
@app.route('/<path:path1>/<path:path2>/<path:path3>')
def serve(path1,path2,path3):
     path = f'/{path1}/{path2}/{path3}'.rstrip('/')
     path_dir = os.path.abspath("./chatbot_ui") #path react build
    #  path_dir = '/home/shujaat/Work/ClouxiPlexi/Training/8_UI_framework_React/flask_react_auth/backend/build'
     full_path=os.path.join(path_dir,path1,path2,path3).rstrip('\\')
     full_path_dir=os.path.join(path_dir,path1,path2).rstrip('\\')
     if path != "" and os.path.exists(full_path):
         if '.' in full_path_dir.split('\\')[-1]:
             path3=full_path_dir.split('\\')[-1]
             full_path_dir=full_path_dir.replace(full_path_dir.split('\\')[-1],'').rstrip('\\')
         return send_from_directory(full_path_dir, path3)
     else:
         return send_from_directory(os.path.join(path_dir),'index.html')

if __name__ == '__main__':
    app.run(debug=True)
