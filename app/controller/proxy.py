from app.controller.controller import Controller
from app.service.proxy import ProxyService
from requests import Response


class ProxyController(Controller):
    def __init__(self, config):
        self.config = config

    def execute(self, need_auth, request, service, path):
        proxy = ProxyService(self.config)
        try:
            data = request.json
        except BaseException:
            data = None

        res = proxy.proxy(need_auth,
                          service,
                          path,
                          request.method,
                          request.headers,
                          data)
        return self._process_response(res)

    def _process_response(self, res):
        if isinstance(res[1], Response):
            return res[1].content, res[1].status_code

        body, status = self.create_response(res, {
            ProxyService.UNKNOWN_SERVICE: ("Unknown Service", 404),
            ProxyService.NEED_AUTHENTICATION: ("Restricted access", 401),
            ProxyService.UNKNOWN_METHOD: ("Method not supported", 405)
        })
        return self.format_response(body), status
