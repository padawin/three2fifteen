import app.factory


def start_app():
    app.factory.create_app().run(port=5004, host='0.0.0.0')


def main():
    start_app()


if __name__ == '__main__':
    start_app()
