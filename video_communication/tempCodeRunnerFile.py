import socket
import pyautogui
import pickle
import struct
import cv2
import numpy as np

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Use UDP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65535)  # Increase receive buffer size

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 5555  # Use a different port if necessary
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Define the scale factor for enlarging the frames
scale_factor = 2.0  # Change this value to enlarge the video (e.g., 2.0 for doubling the size)
frame_rate = 30  # Adjust this value for the desired frame rate

print("Server is listening...")

# Define the target client IP address
target_client_ip = '192.168.0.100'  # Replace with the IP address of the client
target_address = (target_client_ip, port)  # Target address

while True:
    # Capture the screen
    img = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # Resize the frame to a higher resolution
    frame = cv2.resize(frame, 
                       (int(frame.shape[1] * scale_factor), 
                        int(frame.shape[0] * scale_factor)), 
                       interpolation=cv2.INTER_CUBIC)  # Use cubic interpolation
    
    # Serialize and send the frame
    a = pickle.dumps(frame)
    message = struct.pack("Q", len(a)) + a
    
    # Send the frame to the specific client
    server_socket.sendto(message, target_address)  # Send to a specific client
    
    # Display the transmitting screen
    cv2.imshow('TRANSMITTING SCREEN', frame)
    key = cv2.waitKey(1000 // frame_rate) & 0xFF  # Adjust for frame rate
    if key == ord('q'):
        break

server_socket.close()
cv2.destroyAllWindows()
