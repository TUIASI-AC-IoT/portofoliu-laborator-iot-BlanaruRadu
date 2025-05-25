from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DIR = 'dir'
os.makedirs(DIR, exist_ok=True)

#------------------1------------
@app.route('/files', methods=['GET'])
def list_dir():
    return jsonify(os.listdir(DIR))

#------------------2------------
@app.route('/files/<filename>', methods=['GET'])
def read(filename):
    with open(os.path.join(DIR, filename), 'r') as f:
        return jsonify({'content': f.read()})

#------------------3------------
@app.route('/files/<filename>', methods=['PUT'])
def write(filename):
    content = request.json.get('content', '')
    with open(os.path.join(DIR, filename), 'w') as f:
        f.write(content)
    return jsonify({'message': 'OK', 'filename': filename})

#------------------4------------
@app.route('/files', methods=['POST'])
def create():
    data = request.json
    file_path = os.path.join(DIR, data['filename'])
    with open(file_path, 'w') as f:
        f.write(data['content'])
    return jsonify({'message': 'Created', 'filename': data['filename']}), 201

#------------------5------------
@app.route('/files/<filename>', methods=['DELETE'])
def delete(filename):
    os.remove(os.path.join(DIR, filename))
    return jsonify({'message': 'Deleted', 'filename': filename})

#------------------6------------
@app.route('/files/<filename>/update', methods=['PUT'])
def update_file(filename):
    file_path = os.path.join(DIR, filename)

    content = request.json.get('content', '')
    with open(file_path, 'w') as f:
        f.write(content)
    return jsonify({'message': '4444', 'filename': filename})


if __name__ == '__main__':
    app.run()
