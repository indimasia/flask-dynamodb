from flask import Flask, jsonify, request, render_template
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Items')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    item_id = data.get('item_id')
    name = data.get('name')
    try:
        table.put_item(Item={'item_id': item_id, 'name': name})
        return jsonify({'message': 'Item created successfully'}), 201
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        response = table.get_item(Key={'item_id': item_id})
        item = response.get('Item')
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify(item), 200
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    name = data.get('name')
    try:
        response = table.update_item(
            Key={'item_id': item_id},
            UpdateExpression="set #name = :n",
            ExpressionAttributeNames={'#name': 'name'},
            ExpressionAttributeValues={':n': name},
            ReturnValues="UPDATED_NEW"
        )
        return jsonify({'message': 'Item updated successfully', 'attributes': response['Attributes']}), 200
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        table.delete_item(Key={'item_id': item_id})
        return jsonify({'message': 'Item deleted successfully'}), 200
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items', methods=['GET'])
def list_items():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return jsonify(items), 200
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)