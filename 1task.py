import json

from flask import Flask, jsonify, request, abort

app = Flask(__name__)


@app.route('/get-all-interfaces', methods=['GET'])
def get_all_interfaces():
    with open('task-1-interfaces.json') as f:
        data = json.loads(f.read())
        interfaces = data['ietf-interfaces:interfaces']['interface']
    return jsonify(interfaces)


@app.route('/get-interface/<path:interface_name>', methods=['GET'])
def get_some_interface(interface_name):
    with open('task-1-interfaces.json') as f:
        data = json.loads(f.read())
        interfaces = data['ietf-interfaces:interfaces']['interface']
        for interface in interfaces:
            if interface["name"] == interface_name:
                return jsonify(interface)
    abort(404)


@app.route('/get-interfaces', methods=['POST'])
def post_several_interfaces():
    with open('task-1-interfaces.json') as f:
        data = json.loads(f.read())
        req_data = request.get_json()
        interfaces = data['ietf-interfaces:interfaces']['interface']
        result = []
        for interface in interfaces:
            for input_interface in req_data['input']['interfaces']:
                interface_name = input_interface.get('name')
                interface_type = input_interface.get('type')
                interface_enabled = input_interface.get('enabled')
                if (interface_name is None or interface["name"] == interface_name) and \
                        (interface_type is None or interface["type"] == interface_type) and \
                        (interface_enabled is None or interface["enabled"] == interface_enabled):
                    if interface not in result:
                        result.append(interface)
        return jsonify(result)


@app.route('/delete-interface/<path:interface_name>', methods=['DELETE'])
def delete_interface(interface_name):
    with open('task-1-interfaces.json') as f:
        data = json.loads(f.read())
        interfaces = data['ietf-interfaces:interfaces']['interface']
        for interface in interfaces:
            if interface["name"] == interface_name:
                interfaces.remove(interface)
                return jsonify("DELETE was Successful.")
    return jsonify("DELETE was Unsuccessful")


if __name__ == '__main__':
    app.run(debug=True)
