loader.addModule('Socket', 'config', (config) => {
	var socket = null;
	let module = {};

	module.join = (onMessageHooks, gameId) => {
		const protocol = location.protocol == "https:" ? "wss:" : "ws:";
		socket = new WebSocket(
			protocol + "//" + location.hostname + ":" + location.port + "/websocket/"
		);
		socket.onopen = function() {
			module.message({'type': 'join', 'game_id': gameId});
		};

		module.message = function(data) {
			socket.send(JSON.stringify(data));
		}

		socket.onmessage = function(message) {
			var data = JSON.parse(message.data);
			if (!data.type || !onMessageHooks[data.type]) {
				console.log(
					"Socket message received with unknown or no type " + data
				);
				return;
			}

			onMessageHooks[data.type](data);
		};
	};

	return module;
});
