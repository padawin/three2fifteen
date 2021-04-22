loader.addModule('config', () => {
	return {{ data|tojson }};
});
