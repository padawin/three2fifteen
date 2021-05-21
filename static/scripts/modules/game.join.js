loader.executeModule('gameJoinModule',
'config', 'app', 'B', 'request', 'auth', 'utils',
(config, app, B, request, auth, utils) => {
	let module = {
		'action': () => {
			let form = B.$id('game-join-form');
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
						utils.apiResponseHandler(statusCode, body, null, function(body) {
							auth.setToken(body.access_token);
							const game_id = B.$id('game_id').dataset.value;
							let url = config.api_host + config.api_join_game;
							url = utils.format(url, [game_id]);
							request.put(
								url,
								"",
								auth.getHeader(),
								(statusCode, body) => {
									utils.apiResponseHandler(statusCode, body, '/game/' + game_id);
								}
							);
						});
					}
				);
			});
		}
	};
	app.addModule(module);
});
