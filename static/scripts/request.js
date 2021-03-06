loader.addModule('request', () => {
	function _request(method, url, data, headers, doneCallback) {
		var xhr = new XMLHttpRequest();
		xhr.open(method, url);
		for (let header in headers) {
			xhr.setRequestHeader(header, headers[header]);
		}
		xhr.setRequestHeader("Content-type", "application/json");
		xhr.onreadystatechange = (e) => {
			if (e.target.readyState == 4) {
				doneCallback(e.target.status, JSON.parse(e.target.response));
			}
		};
		xhr.send(data);
	}

	return {
		post: (url, data, headers, doneCallback) => {
			_request("POST", url, data, headers, doneCallback);
		},
		put: (url, data, headers, doneCallback) => {
			_request("PUT", url, data, headers, doneCallback);
		},
		get: (url, headers, doneCallback) => {
			_request("GET", url, null, headers, doneCallback);
		}
	};
});
