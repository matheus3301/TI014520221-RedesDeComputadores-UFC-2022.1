import socket
import logging
import threading


class Server:
    def __init__(self, config) -> None:

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s')

        self.__config = config

        # receiving tcp connections
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((self.__config["HOST"], self.__config["PORT"]))
        self.connection.listen(10)

        logging.info(
            f"server is avaliable on {self.__config['HOST']}:{self.__config['PORT']}")

        while True:
            try:
                (client_socket, client_address) = self.connection.accept()

                # for each new connection, a new thread to solve the request is created
                thread = threading.Thread(
                    target=self.request_thread, args=(client_socket, client_address))

                # setting the thread as daemon, to die with its parent
                thread.setDaemon(True)

                thread.start()
            except KeyboardInterrupt:
                logging.info(f"server is shutting down")
                self.connection.close()
                exit()

    def request_thread(self, client_socket, client_address):
        logging.info(f"new request from {client_address}")

        request = client_socket.recv(self.__config['BUFFER_SIZE']).decode()

        logging.debug(request)

        # handling http string

        # getting the first line, where is possible to see the requested url
        request_first_line = request.split('\n')[0]

        # METHOD URL HTTP-VERSION
        requested_url = request_first_line.split(' ')[1]

        http_pos = requested_url.find("://")

        logging.debug(requested_url)

        if http_pos == -1:
            tmp = requested_url
        else:

            # removing www
            tmp = requested_url[(http_pos+3):]

        logging.debug(tmp)

        port_pos = tmp.find(":")

        webserver_pos = tmp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(tmp)

        webserver = ""
        port = -1
        if (port_pos == -1 or webserver_pos < port_pos):

            # if there is not a specific port, the default is the 80
            port = 80
            webserver = tmp[:webserver_pos]

        else:
            port = int((tmp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = tmp[:port_pos]

        if webserver in self.__config["DENY_LIST"]:
            logging.info("requested url is forbidden by the deny list")
            client_socket.send(self.get_denied_message().encode())
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()

            return

        logging.info(f"starting request to {webserver}:{port}")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.__config['CONNECTION_TIMEOUT'])
        s.connect((webserver, port))
        s.sendall(request.encode())

        while True:
            try:
                data = s.recv(self.__config['BUFFER_SIZE'])

                if len(data) > 0:
                    client_socket.send(data)
                else:
                    s.close()
                    break
            except TimeoutError:
                s.close()
                break

        client_socket.close()

    def get_denied_message(self):
        path = "./server/src/static/denied.html"
        f = open(path, 'r')
        page = f.read()
        f.close()

        return page
