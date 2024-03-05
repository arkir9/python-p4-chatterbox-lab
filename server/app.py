from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET' , 'POST'])
def messages():
    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            messaage_dict = message.to_dict()
            messages.append(messaage_dict)
        
        response = make_response(
            jsonify(messages),
            200
        )
        return response
    elif request.method == 'POST':
        body = request.get_json()['body']
        username = request.get_json()['username']
        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()
        message_dict = new_message.to_dict()
        response = make_response(
            jsonify(message_dict),
            201)
        return response
@app.route('/messages/<int:id>', methods = ['PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    if request.method == 'PATCH':
        body = request.json.get('body')
        if not body:
            return jsonify({'error': 'Body is required'}), 400
        message.body = body
        db.session.commit()
        return jsonify(message.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555)
