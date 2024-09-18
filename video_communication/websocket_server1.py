import asyncio
import websockets
import pyautogui
import pickle
import cv2
import numpy as np
import imutils

# Define the scale factor for enlarging the frames
scale_factor = 1.5  # Adjust the scale factor

async def send_video(websocket, path):
    while True:
        # Capture the screen
        img = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Resize the frame to a lower resolution
        frame = imutils.resize(frame, width=320)  # Reduce the width to reduce frame size
        
        # Optionally enlarge the frame using high-quality resampling
        frame = cv2.resize(frame, 
                           (int(frame.shape[1] * scale_factor), 
                            int(frame.shape[0] * scale_factor)), 
                           interpolation=cv2.INTER_CUBIC)
        
        # Serialize the frame
        data = pickle.dumps(frame)
        
        # Send the serialized data over WebSocket
        await websocket.send(data)
        
        # Display the transmitting screen
        cv2.imshow('TRANSMITTING SCREEN', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

async def main():
    async with websockets.serve(send_video, "localhost", 9999):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
