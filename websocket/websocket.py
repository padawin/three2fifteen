import json
import logging
from tornado.websocket import WebSocketHandler


def _get_status(socket, data):
    logger = logging.getLogger(__name__)
    try:
        game_id = data['game_id']
    except KeyError:
        logger.error("No game found in data")
        return
    try:
        room = WebSocket._game_rooms[game_id]
    except KeyError:
        logger.error("no room found for game id: {}".format(game_id))

    if socket not in room:
        socket.write_message(json.dumps(
            {'type': 'status', 'message': 'Socket not in room'}
        ))
    else:
        socket.write_message(json.dumps(
            {
                'type': 'status',
                'message': 'Socket in room with {} other sockets'.format(len(room)-1)
            }
        ))


def _join_game(socket, data):
    logger = logging.getLogger(__name__)
    logger.info("Try join game, %s", data)
    try:
        game_id = data['game_id']
    except KeyError:
        return

    print(WebSocket._game_rooms)
    try:
        room = WebSocket._game_rooms[game_id]
    except KeyError:
        room = []

    for s in room:
        if s != socket:
            s.write_message(json.dumps({'type': 'player-joined'}))

    socket.game_id = game_id
    room.append(socket)
    logger.info("Socket joined %s", socket.game_id)
    logger.info("Number clients in room: %s", len(room))
    WebSocket._game_rooms[game_id] = room


def _broadcast_play(socket, data):
    try:
        room = WebSocket._game_rooms[socket.game_id]
    except KeyError:
        return

    for s in room:
        if s != socket:
            s.write_message(json.dumps({'type': 'player-played'}))


def _leave_game(socket):
    WebSocket._game_rooms[socket.game_id].remove(socket)


class WebSocket(WebSocketHandler):
    _game_rooms = {}

    _actions_mapping = {
        "join": _join_game,
        "play": _broadcast_play,
        "status": _get_status
    }

    def open(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info("Socket opened")
        self.write_message('"hello world"')

    def on_message(self, message):
        """
        message is a string containing a json dump. The json is expected to
        contain a "type" key telling which type of message is received, and
        potentially other keys, depending on the type
        """
        try:
            data = json.loads(message)
            message_type = data['type']
        except json.JSONDecodeError:
            self._logger.error("Invalid message received: {}".format(message))
            return
        except KeyError:
            self._logger.error(
                "Invalid message format received, type missing: {}".format(
                    message
                )
            )
            return

        try:
            action = self._actions_mapping[message_type]
        except KeyError:
            self._logger.error(
                "Invalid message type: {}".format(message_type)
            )
            return

        action(self, data)

    def on_close(self):
        self._logger.info("Socket closed")
        _leave_game(self)
