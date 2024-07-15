from flask import Flask, render_template,request, jsonify,redirect,url_for
from dotenv import load_dotenv
from db.db_api import DbApi
import os
import json

load_dotenv()
app = Flask(__name__,template_folder="templates")
db_api = DbApi()
DB_NAME = os.getenv("DB_NAME")
LOG_COLLECTION = os.getenv("BD_LOG_COLLECTION")
RET_OK =0
db_api.init(DB_NAME)

@app.route('/')
def home():
    return render_template('dashbord.html')

@app.route('/watchers')
def watchers():
    log_collection = db_api.get_collection(DB_NAME,LOG_COLLECTION)
    print(f"{log_collection=}")
    return render_template('watchers.html',items=log_collection)

@app.route('/submit_new_log', methods=['POST'])
def submit_new_log():
    print(f"submit_new_log")
    json_rsp = request.form.to_dict()
    print(f"submit_new_log {json_rsp=}")
    if db_api.insert_document(DB_NAME,LOG_COLLECTION,json_rsp) == RET_OK:
        return jsonify({'message': f'Form submitted {json_rsp}'})
    return jsonify({'message': f'Failed to submit {json_rsp}'})

@app.route('/delete_event', methods=['POST'])
def delete_event():
    json_rsp = request.form.to_dict()
    print(f"delete_event {json_rsp=}")
    if db_api.delete_document(DB_NAME,LOG_COLLECTION,json_rsp['item_id']) ==RET_OK:
        return jsonify({'message': f'Event deleted {json_rsp["item_id"]}'})
    return jsonify({'message': f'Event deleted Error {json_rsp["item_id"]}'})

if __name__ == '__main__':
    print("running main")
    app.run(debug=True,port=5001)
