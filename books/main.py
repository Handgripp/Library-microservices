from src.app import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5003, debug=True)