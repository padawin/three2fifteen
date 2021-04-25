loader.executeModule('headerModule',
'B', 'auth', 'utils', 'app',
(B, auth, utils, app) => {
	app.addModule({
		'action': () => {
			B.$id('logout-button').addEventListener('click', (e) => {
				e.preventDefault();
				console.log("here");
				auth.unsetToken();
				utils.goToUrl('/');
			});
		}
	});
});
