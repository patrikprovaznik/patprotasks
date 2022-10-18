import http
import json
from configparser import ConfigParser
from flask import Flask, jsonify, request, Response

config = ConfigParser()
config.read("flask_app_config.ini")


class InterfaceAPI(Flask):
    def __init__(self, import_name: str):
        super(InterfaceAPI, self).__init__(import_name)
        with open('resource/task-1-interfaces.json') as f:
            data = json.loads(f.read())
            interfaces = data['ietf-interfaces:interfaces']['interface']
            self.cache = {interface['name']: interface for interface in interfaces}


app = InterfaceAPI(__name__)


@app.route('/get-all-interfaces', methods=['GET'])
def get_all_interfaces() -> Response:
    all_interfaces = app.cache.values()
    return jsonify(list(all_interfaces))


@app.route('/get-interface/<path:interface_name>', methods=['GET'])
def get_some_interface(interface_name: str) -> Response | tuple[Response, int]:
    interface = app.cache.get(interface_name)
    if interface:
        return jsonify(interface)
    else:
        return jsonify({interface_name: {'info': 'interface does not exist'}}), http.HTTPStatus.NOT_FOUND


@app.route('/get-interfaces', methods=['POST'])
def post_several_interfaces() -> Response:
    all_interfaces = app.cache.values()
    req_data = request.get_json()
    result = []
    for input_interface in req_data['input']['interfaces']:
        interface_name = input_interface.get("name")
        interface_type = input_interface.get("type")
        interface_enabled = input_interface.get("enabled")
        if (interface_by_name := app.cache.get(interface_name)) and \
                (interface_type is None or interface_by_name.get("type") == interface_type) and \
                (interface_enabled is None or interface_by_name.get("enabled") == interface_enabled):
            result.append(interface_by_name)
        else:
            for interface in all_interfaces:
                if (interface_type is None or interface.get("type") == interface_type) and \
                        (interface_enabled is None or interface.get("enabled") == interface_enabled):
                    result.append(interface)
    return jsonify(result)


@app.route('/delete-interface/<path:interface_name>', methods=['DELETE'])
def delete_interface(interface_name: str) -> tuple[Response, int]:
    interface_deleted = app.cache.pop(interface_name, None)
    if interface_deleted:
        return jsonify({interface_name: {'info': 'DELETE WAS SUCCESSFUL'}}), http.HTTPStatus.OK
    else:
        return jsonify(
            {interface_name: {'info': 'DELETE WAS UNSUCCESSFUL, interface does not exist'}}), http.HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    app.config['SECRET_KEY'] = config['flask']['secret_key']
    app.run(debug=True, host=config['flask']['host'], port=int(config['flask']['port']))
