import logging
import jwt
import uuid

from api.controller.controller import Controller


class PlayerController(Controller):
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(config['APP_NAME'])

    def login(self, request):
        try:
            data = request.get_json()
        except BaseException:
            data = None

        if data is None or 'username' not in data or data['username'] == '':
            return self.format_response({
                'message': "username required"
            }), 400

        body = {
            'access_token': jwt.encode({
                    'username': data['username'],
                    'id_player': str(uuid.uuid1())
                },
                self.config['SECRET_KEY'],
                algorithm='HS256'
            )
        }
        return self.format_response(body), 200
