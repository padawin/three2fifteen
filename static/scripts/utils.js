loader.addModule('utils', 'B', (B) => {
	const utils = {
		apiResponseHandler: (statusCode, body, toUrl, callback) => {
			if (statusCode == 200) {
				if (callback) {
					callback(JSON.parse(body));
				}
				utils.goToUrl(toUrl);
			}
			else {
				B.$id("form-message").innerHTML = JSON.parse(body).message;
			}
		},
		goToUrl: (to) => {
			window.location.replace(to);
		},
		// VERY Quick and dirty string formating
		format: (str, args) => {
			for (let replace of args) {
				str = str.replace("%s", replace);
			}
			return str;
		}
	};

	return utils;
});
