import socket
import threading
import logging
from src.messages import Message

HOSTNAME = 'localhost'
PORT = 3333
BUFFER_SIZE = 4096

queue = []
pair = {}


def main():
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.bind((HOSTNAME, PORT))

    message_handling = threading.Thread(target=handle_messages, args=(server,))
    queue_processing = threading.Thread(target=process_queue, args=(server,))

    message_handling.start()
    queue_processing.start()


def handle_messages(server: socket):
    while True:
        message, address = server.recvfrom(BUFFER_SIZE)
        message = message.decode()

        if message == Message.JOIN.value:
            queue.append(address)
            # server.sendto(Message.ACK.value.encode(), address)
        elif message == Message.LEAVE.value:
            queue.remove(address)
            # server.sendto(Message.ACK.value.encode(), address)
        elif pair.get(address) != None:
            server.sendto(message, pair.get(address))
            # server.sendto()
            # TODO: Send image to the other person
            print("Sending to it pair")
        else:
            server.sendto(Message.ERROR.value.encode(), address)


def process_queue(server: socket):
    while True:
        if len(queue) >= 2:  # at least two people waiting for a meet
            a = queue[0]
            del queue[0]

            b = queue[0]
            del queue[0]

            pair[a] = b
            pair[b] = a

            server.sendto(Message.MEET.value.encode(), a)
            server.sendto(Message.MEET.value.encode(), b)


if __name__ == "__main__":
    main()
