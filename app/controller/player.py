from app.model.player import PlayerModel
from app.service.player import PlayerService
from app.controller.controller import Controller
import json


class PlayerController(Controller):
    def get_names(self, request, user_ids):
        identity = json.loads(request.headers['X-User'])
        ps = PlayerService(PlayerModel)
        names = ps.get_names(user_ids)
        names[identity['user_id']] = 'You'
        return self.format_response(names)
