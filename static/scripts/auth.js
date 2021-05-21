loader.addModule('auth',
() => {
	const TOKEN_KEY = 'JWT';
	const GAME_KEY = 'CURRENT_GAME';
	return {
		'setToken': (token) => {
			window.localStorage.setItem(TOKEN_KEY, token);
		},
		'getToken': () => {
			return window.localStorage.getItem(TOKEN_KEY);
		},
		'unsetToken': () => {
			window.localStorage.removeItem(TOKEN_KEY);
		},
		'isLoggedIn': () => {
			return window.localStorage.getItem(TOKEN_KEY) != null;
		},
		'getHeader': () => {
			return {'X-Token': window.localStorage.getItem(TOKEN_KEY)}
		},
		'setGameID': (gameID) => {
			window.localStorage.setItem(GAME_KEY, gameID);
		},
		'getGameID': () => {
			return window.localStorage.getItem(GAME_KEY);
		}
	};
});
