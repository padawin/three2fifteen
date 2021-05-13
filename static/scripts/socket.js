loader.addModule('Socket', 'config', (config) => {
	var socket = null;
	let module = {};

	let waitForSocketConnection = function(socket, callback){
		setTimeout(function() {
			if (socket.readyState === 1) {
				console.log("Connection is made")
			} else if (socket.readyState == 3) {
				if (callback != null){
					callback();
				}
			} else {
				console.log("wait for connection...")
				waitForSocketConnection(socket, callback);
			}
		}, 5);
	}

	module.join = (onMessageHooks, gameId, failCallback) => {
		const protocol = location.protocol == "https:" ? "wss:" : "ws:";
		socket = new WebSocket(
			protocol + "//" + location.hostname + ":" + location.port + "/websocket/"
		);
		socket.onopen = function() {
			module.message({'type': 'join', 'game_id': gameId});
		};

		module.message = function(data) {
			if (socket.readyState == 0) {
				socket.send(JSON.stringify(data));
			}
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

		waitForSocketConnection(socket, failCallback);
	};

	return module;
});
