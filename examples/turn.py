from app.model.model import Model
Model.connect("dbname=three2fifteen_game user=postgres host=172.17.0.2 password=mysecretpassword")
from app.service.turn import TurnService
from app.model.game import GameModel
from app.model.game_player import GamePlayerModel
from app.model.turn import TurnModel
ts = TurnService(GameModel, TurnModel, GamePlayerModel)
res = ts.turn(1, 2, [])
print(res)
res = ts.turn(1, 3, [])
print(res)
res = ts.turn(1, 1, [])
print(res)
res = ts.turn(1, 1, [1])
print(res)
res = ts.turn(1, 1, [{'x': 1, 'y': 1, 'value': 10}])
print(res)
res = ts.turn(1, 1, [{'x': 1, 'y': 1, 'value': 2}])
print(res)
res = ts.turn(1, 1, [{'x': 7, 'y': 7, 'value': 2}])
print(res)
