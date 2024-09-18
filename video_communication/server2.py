# Import the libraries
import socket
import pyautogui
import pickle
import struct
import cv2
from PIL import Image
import imutils
import numpy as np

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

# Define the scale factor for enlarging the frames
scale_factor = 2.0  # Change this value to enlarge the video (e.g., 2.0 for doubling the size)

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        while True:
            # Capture the screen
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # Resize the frame
            frame = imutils.resize(frame, width=320)  # Resize to a standard width
            frame = cv2.resize(frame, (int(frame.shape[1] * scale_factor), int(frame.shape[0] * scale_factor)))  # Enlarge the frame
            
            # Serialize and send the frame
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            
            # Display the transmitting screen
            cv2.imshow('TRANSMITTING SCREEN', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break
