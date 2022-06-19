import socket
import threading
import cv2
import pickle
import struct

from src.messages import Message


msgFromClient = Message.JOIN.value.encode()
bytesToSend = msgFromClient
server_ip = ("127.0.0.1", 3333)
bufferSize = 4096


def handle_external_Video(client: socket):
    data = ""
    payload_size = struct.calcsize("H")

    while True:
        client.recvfrom(bufferSize)
        while len(data) < payload_size:
            data += client.recv(bufferSize)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("H", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

        frame = pickle.loads(frame_data)
        cv2.imshow('Other', frame)


def handle_user_video(client: socket):
    vid = cv2.VideoCapture(0)

    while(True):
        ret, frame = vid.read()
        cv2.imshow("You", frame)

        data_to_send = pickle.dumps(frame)
        client.sendall(struct.pack("H", len(data_to_send)) + data_to_send)

        # k = cv2.waitKey(30) & 0xff
        # if k == 27:
        #     break

    # vid.release()
    # cv2.destroyAllWindows()


# Create a UDP socket at client side
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Send to server using created UDP socket
client.sendto(bytesToSend, server_ip)

msgFromServer = client.recvfrom(bufferSize)
print(msgFromServer)
msg = msgFromServer[0].decode()
print(msg)


# a = threading.Thread(target=handle_external_Video, args=(client,))
# a.start()


if msg == Message.MEET.value:
    a = threading.Thread(target=handle_external_Video, args=(client,))
    b = threading.Thread(target=handle_user_video, args=(client,))

    a.start()
    b.start()

else:
    print("Error!")
