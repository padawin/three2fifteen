import json


class Controller(object):
    def format_response(self, response):
        return json.dumps(response)

    def create_response(self, service_result, cases):
        # no cases can be considered as fine
        if not isinstance(cases, dict):
            return {}, 200
        # if the result is True, returns 200
        elif service_result[0]:
            if 0 in cases:
                return cases[0](service_result[1]), 200
            else:
                return {}, 200
        elif service_result[1] in cases:
            return {'message': cases[service_result[1]][0],
                    'code': service_result[1]}, cases[service_result[1]][1]
        else:
            return {'message': "Unknown error"}, 500
