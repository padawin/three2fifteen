loader.executeModule('homeModule',
'config', 'app', 'B', 'Game', 'request', 'utils', 'auth',
(config, app, B, Game, request, utils, auth) => {
	let module = {
		'action': () => {
			let form = B.$id('game-creation-form');
			form.addEventListener('submit', (e) => {
				B.$id("form-message").innerHTML = "";
				e.preventDefault();
				request.post(
					config.api_host + config.api_login,
					JSON.stringify({
						'username': form.player_name.value,
					}),
					{},
					(statusCode, body) => {
						if (statusCode != 200) {
							B.$id("form-message").innerHTML = body.message;
							return;
						}
						auth.setToken(body.access_token);
						request.post(
							config.api_host + config.api_create_game,
							JSON.stringify({
								'number_players': form.nbPlayers.value
							}),
							auth.getHeader(),
							(statusCode, body) => {
								utils.apiResponseHandler(statusCode, body, '/game/' + body.game_id);
							}
						);
					}
				);
			});
		}
	};
	app.addModule(module);
});
