import http
import json

from flask import Flask, jsonify, request, Response


class InterfaceAPI(Flask):
    def __init__(self, import_name):
        super(InterfaceAPI, self).__init__(import_name)
        self.cache = {}
        with open('resource/task-1-interfaces.json') as f:
            data = json.loads(f.read())
            interfaces = data['ietf-interfaces:interfaces']['interface']
            for interface in interfaces:
                self.cache[interface['name']] = interface


app = InterfaceAPI(__name__)


@app.route('/get-all-interfaces', methods=['GET'])
def get_all_interfaces() -> Response:
    all_interfaces = app.cache.values()
    return jsonify(list(all_interfaces))


@app.route('/get-interface/<path:interface_name>', methods=['GET'])
def get_some_interface(interface_name: str) -> Response | tuple[str, int]:
    interface = app.cache.get(interface_name)
    if interface:
        return jsonify(interface)
    else:
        return '', http.HTTPStatus.NOT_FOUND


@app.route('/get-interfaces', methods=['POST'])
def post_several_interfaces() -> Response:
    all_interfaces = app.cache.values()
    req_data = request.get_json()
    result = []
    for interface in all_interfaces:
        for input_interface in req_data['input']['interfaces']:
            interface_name = input_interface.get("name")
            interface_type = input_interface.get("type")
            interface_enabled = input_interface.get("enabled")
            if (interface_name is None or interface["name"] == interface_name) and \
                    (interface_type is None or interface["type"] == interface_type) and \
                    (interface_enabled is None or interface["enabled"] == interface_enabled):
                if interface not in result:
                    result.append(interface)
    return jsonify(result)


@app.route('/delete-interface/<path:interface_name>', methods=['DELETE'])
def delete_interface(interface_name: str) -> tuple[str, int]:
    interface_deleted = app.cache.pop(interface_name, None)
    if interface_deleted:
        return 'DELETE was Successful', http.HTTPStatus.OK
    else:
        return 'DELETE was Unsuccessful.', http.HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    app.run(debug=True)
