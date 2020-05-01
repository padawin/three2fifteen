from app.identity import Identity
import requests
import json
import logging


class ProxyService(object):
    UNKNOWN_METHOD = 1
    UNKNOWN_SERVICE = 2
    UNKNOWN_ERROR = 3
    NEED_AUTHENTICATION = 4

    valid_methods = {
        'GET': 'get',
        'POST': 'post',
        'DELETE': 'delete',
        'PUT': 'put'
    }

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.config['APP_NAME'])

    def proxy(self, need_auth, service, path, method='GET', headers={}, data={}, params={}):
        services_key = 'SERVICES'
        if (
            service not in self.config[services_key] or
            self.config[services_key][service]['need_auth'] != need_auth
        ):
            return (False, ProxyService.UNKNOWN_SERVICE)

        if need_auth:
            headers = dict(headers)
            identity = Identity.get(headers, self.config)
            if identity is None:
                return (False, ProxyService.NEED_AUTHENTICATION)

            headers['X-User'] = json.dumps(identity)

        url = "{}{}".format(self.config['SERVICES'][service]['base'], path)

        res = self._call(url, method, headers, data, params)
        if not res[0] and isinstance(res[1], dict):
            self.logger.error(res[1])
            return (False, ProxyService.UNKNOWN_ERROR)

        return res

    def _call(self, url, method='GET', headers={}, data={}, params={}):
        method = method.upper()
        if method not in ProxyService.valid_methods:
            return (False, ProxyService.UNKNOWN_METHOD)
        method = getattr(requests, ProxyService.valid_methods[method])

        custom_headers = dict(headers)
        if 'Content-type' not in custom_headers:
            custom_headers['Content-type'] = 'application/json'

        try:
            response = method(
                url,
                data=json.dumps(data),
                params=params,
                headers=custom_headers
            )
        except requests.exceptions.RequestException as e:
            return (False, {'error': e})

        return (response.status_code == 200, response)
