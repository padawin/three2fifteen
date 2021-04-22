from flask import current_app


class ConfigController(object):
    def get(self):
        return {
            'api_host': current_app.config['API_HOST'],
            'api_login': current_app.config['API_LOGIN'],
            'api_signup': current_app.config['API_SIGNUP'],
            'api_get_games': current_app.config['API_GET_GAMES'],
            'api_get_game': current_app.config['API_GET_GAME'],
            'api_create_game': current_app.config['API_CREATE_GAME'],
            'api_join_game': current_app.config['API_JOIN_GAME'],
            'api_get_board': current_app.config['API_GET_BOARD'],
            'api_get_game_content': current_app.config['API_GET_GAME_CONTENT'],
            'api_get_hand': current_app.config['API_GET_HAND'],
            'api_turn_check': current_app.config['API_TURN_CHECK'],
            'api_turn': current_app.config['API_TURN'],
            'api_get_player_names': current_app.config['API_GET_PLAYER_NAMES']
        }
