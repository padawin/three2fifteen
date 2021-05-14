loader.executeModule('gamePageModule',
'config', 'app', 'B', 'utils', 'Game', 'Socket', 'request', 'auth',
(config, app, B, utils, Game, Socket, request, auth) => {
	const gameId = B.$id('game_id').dataset.value;

	const getTDNode = (node) => {
		while (node && node.nodeName != 'TD') {
			node = node.parentNode;
		}
		return node;
	};

	let _hoveredCell = null;
	const _tokenOverHand = (e) => {
		e.preventDefault();
	}

	const _postMove = (valid, message, enableConfirm) => {
		let cpNode = B.$id('confirm-play'),
			alertNode = B.$id('alert-container');
		alertNode.innerHTML = message;
		if (message) {
			B.removeClass(alertNode, 'hidden');
		}
		else {
			B.addClass(alertNode, 'hidden');
		}

		if (valid) {
			B.addClass(alertNode, 'alert-success');
			B.removeClass(alertNode, 'alert-danger');
		}
		else {
			B.removeClass(alertNode, 'alert-success');
			B.addClass(alertNode, 'alert-danger');
		}

		if (enableConfirm) {
			cpNode.removeAttribute('disabled');
		}
		else {
			cpNode.setAttribute('disabled', 'disabled');
		}
	};

	const _tokenOverBoard = (e) => {
		B.removeClass(_hoveredCell, 'hovered');
		_hoveredCell = e.target;
		B.addClass(_hoveredCell, 'hovered');
		e.preventDefault();
	}

	const _refresh = () => {
		app.getModuleData(
			module,
			module.dataUrls.slice(),
			_render,
			new Set(['game_content', 'game', 'player_hand'])
		);
	};

	const _resultMove = (move, dryRun) => {
		move.then((score) => {
			_postMove(true, score, dryRun);
			if (!dryRun) {
				// fetch data back
				_refresh();
				if (config.use_socket) {
					Socket.message({'type': 'play'});
				}
			}
		}).catch((message) => {
			_postMove(false, message, false);
		});
	};

	const _dropToken = (e, callback) => {
		e.preventDefault();
		const li = getTDNode(e.target);
		const token = B.$id(e.dataTransfer.getData('token-id'));
		// Prevent from dropping more than one token in the same space
		if (li.children.length) {
			return;
		}
		li.appendChild(token);
		const move = callback(token, li);
		_resultMove(move, true);
		B.removeClass(_hoveredCell, 'hovered');
		_hoveredCell = e.target;
	};

	const _dropTokenHand = (e) => {
		e.preventDefault();
		const token = B.$id(e.dataTransfer.getData('token-id'));
		B.$id('player-hand').appendChild(token);
		const move = Game.removeToken(
			gameId,
			token.id
		);
		if (move) {
			_resultMove(move, true);
		}
		else {
			_postMove(true, '', false);
		}
		B.removeClass(_hoveredCell, 'hovered');
	};

	const _dropTokenBoard = (e) => {
		_dropToken(e, (token, li) => {
			return Game.placeToken(
				gameId,
				token.id,
				parseInt(li.dataset.x),
				parseInt(li.dataset.y),
				parseInt(token.dataset.value)
			);
		});
	};

	const _prepareData = () => {
		let template;
		Game.analyseGame(module.data.game);
		if (module.data.game.open) {
			template = 'game_open';
			module.data.host = window.location.protocol + '//' + window.location.host;
		}
		else if (module.data.game.ongoing) {
			template = 'game_ongoing';
			module.data.game.size_bag = module.data.game_content.size_bag;
			Game.setBoardContent(
				module.data.board,
				module.data.game_content.tokens
			);
			module.data.player_hand.forEach((token, index) => {
				module.data.player_hand[index] = {'value': token, 'index': index};
			});
		} else {
			template = 'game_finished';
			Game.findWinner(module.data.game);
		}
		return template;
	};

	const _render = () => {
		let template = _prepareData();

		B.$id('game-section').innerHTML = B.Template.compile(
			template,
			module.data
		);

		_setEvents();
	};

	const _setEvents = () => {
		if (module.data.game.open) {
			B.$id("copy-link-btn").addEventListener('click', (e) => {
				e.preventDefault();
				let field = B.$id(e.target.getAttribute('rel'));
				B.removeClass(field, "hidden");
				field.select();
				document.execCommand("Copy");
			});
		}
		else if (module.data.game.ongoing) {
			// Set events
			document.querySelectorAll('#player-hand .token').forEach((token) => {
				token.addEventListener('dragstart', (e) => {
					e.dataTransfer.setData('token-id', token.id);
				});
			});
			B.$id('player-hand').addEventListener('dragover', _tokenOverHand);
			B.$id('player-hand').addEventListener('drop', _dropTokenHand);
			document.querySelectorAll('#board td').forEach((place) => {
				place.addEventListener('dragover', _tokenOverBoard, false);
				place.addEventListener('drop', _dropTokenBoard, false);
			});
			B.$id('confirm-play').addEventListener('click', (e) => {
				e.preventDefault();
				e.preventDefault();
				const play = Game.play(gameId);
				_resultMove(play, false);
			});
		}
	};

	// Callback to setup a manual periodic call to the server, to know whether
	// the game changed.
	// This is used as a fallback when WebSocket do not work.
	let gameStatus = null;
	let observeGameChanges = function() {
		let isPolling = false;
		setInterval(function() {
			if (isPolling) {
				return;
			}
			isPolling = true;
			request.get(
				config.api_host + utils.format(config.api_get_game_status, [gameId]),
				auth.getHeader(),
				(response_status, response) => {
					isPolling = false;
					if (response_status != 200) {
						return;
					}

					if (gameStatus !== response) {
						gameStatus = response;
						_refresh();
					}
				}
			);
		}, 1000);
	};

	let module = {
		'dataUrls': [
			{'url': config.api_get_board, 'name': 'board'},
			{'url': utils.format(config.api_get_game_content, [gameId]), 'name': 'game_content'},
			{'url': utils.format(config.api_get_game, [gameId]), 'name': 'game'},
			{'url': utils.format(config.api_get_hand, [gameId]), 'name': 'player_hand'}
		],
		'action': () => {
			B.Template.init({
				game_ongoing: {html: B.$id('game-ongoing').innerHTML},
				game_open: {html: B.$id('game-open').innerHTML},
				game_finished: {html: B.$id('game-finished').innerHTML},
				player_token: {html: B.$id('player-token').innerHTML},
				board_token: {html: B.$id('board-token').innerHTML},
				board_cell: {html: B.$id('board-cell').innerHTML},
				board_row: {html: B.$id('board-row').innerHTML},
				player_score: {html: B.$id('template-player-score').innerHTML},
				game_creator: {html: B.$id('template-game-creator').innerHTML},
				player_turn: {html: B.$id('template-player-turn').innerHTML},
				winner_token: {html: B.$id('winner-token').innerHTML}
			});

			if (config.use_socket) {
				console.log("Use WebSocket");
				Socket.join(
					{
						'player-played': _refresh,
						'player-joined': _refresh,
					},
					gameId
				);
			}
			else {
				console.log("Use Periodic polling");
				observeGameChanges();
			}
			// Render page
			_render();
		}
	};
	app.addModule(module);
});
