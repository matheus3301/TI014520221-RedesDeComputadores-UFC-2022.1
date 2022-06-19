import socket
import threading
import imutils
import cv2
import pickle

from src.messages import Message

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

vid = cv2.VideoCapture(1)

msgFromClient       = Message.JOIN.value.encode()
bytesToSend         = msgFromClient
serverAddressPort   = ("127.0.0.1", 3333)
bufferSize          = 2048 

def get_video_from_meet(client : socket):
    pass

def send_video_to_meet(client : socket):
    global vid

    while(True):
        ret, frame = vid.read()
        frame = imutils.resize(frame, width=320)
        result, image = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(image, 0)
        client.sendto(data, serverAddressPort)



# Create a UDP socket at client side
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 

# Send to server using created UDP socket
client.sendto(bytesToSend, serverAddressPort)

msgFromServer = client.recvfrom(bufferSize)
print(msgFromServer)
msg = msgFromServer[0].decode()
print(msg)

if msg == Message.MEET.value:
    a = threading.Thread(target=get_video_from_meet, args=(client,))
    b = threading.Thread(target=send_video_to_meet, args=(client,))
    

    a.start()
    b.start()

else:
    print("Error!")

