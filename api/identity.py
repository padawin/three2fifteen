import jwt


class Identity(object):
    @staticmethod
    def get(headers, config):
        if 'X-Token' not in headers:
            return None

        try:
            decoded = jwt.decode(headers['X-Token'],
                                 config['SECRET_KEY'],
                                 algorithms=['HS256'])
        except jwt.exceptions.DecodeError:
            return None

        del headers['X-Token']
        return decoded
