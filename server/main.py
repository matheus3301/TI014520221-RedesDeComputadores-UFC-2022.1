from src.server import Server


def main():
    config = {
        "CONNECTION_TIMEOUT": 50,
        "HOST": 'localhost',
        "PORT": 7777,
        "BUFFER_SIZE": 1024,
        "DENY_LIST": ["www.quadrix.org.br", "httpforever.com", "captive.apple.com"]
    }

    Server(config=config)


if __name__ == "__main__":
    main()
