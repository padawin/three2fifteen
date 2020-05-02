import sys
from app.model.model import Model
from app.model.game import GameModel
from app.model.game_player import GamePlayerModel
from app.model.turn import TurnModel
from app.model.player import PlayerModel
from app.service.player import PlayerService
from app.service.game import GameService
from app.service.turn import TurnService

Model.connect("dbname=three2fifteen_game user=postgres host=172.17.0.2 password=mysecretpassword")
# add players
ps = PlayerService(PlayerModel)
playerId1 = ps.create(1)
playerId1Bis = ps.create(1)
playerId2 = ps.create(2)
playerId3 = ps.create(3)
playerId4 = ps.create(4)
print(playerId1, playerId2, playerId3, playerId4, playerId1Bis)

if (not playerId1[0] or
    not playerId2[0] or
    not playerId3[0] or
    not playerId4[0] or
    playerId1Bis[0]
):
    print("Error in player creation")
    sys.exit(1)

playerId1 = playerId1[1]
playerId2 = playerId2[1]
playerId3 = playerId3[1]
playerId4 = playerId4[1]

gs = GameService(GameModel, GamePlayerModel)
# create first game
game1Id = gs.create(playerId1, 3)
res = gs.addPlayer(game1Id, playerId2)
print("Result add player 2: {}".format(res))
print("game {} created from {}, guest: {}".format(game1Id, playerId1, playerId2))
res = gs.addPlayer(game1Id, playerId3)

# create second game
game2Id = gs.create(playerId3, 2)
res = gs.addPlayer(game2Id, playerId1)
print("Result add player 1: {}".format(res))
res = gs.addPlayer(game2Id, playerId4)
print("Result add player 4: {}".format(res))
print("game {} created from {}, guest: {}, ".format(game2Id, playerId3, playerId1, playerId4))
gamesOf1 = GamePlayerModel.loadGamesFromPlayerId(playerId1)
print("Player 1 plays the following games:")
print(gamesOf1)

Model.disconnect()
