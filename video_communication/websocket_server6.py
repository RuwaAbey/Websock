import asyncio
import websockets
import pyautogui
import cv2
import numpy as np
import pickle

# Use a higher resolution and compression
frame_width = 640  # Increase the frame width
jpeg_quality = 80   # JPEG quality (1-100, where 100 is the best)

async def send_video(websocket, path):
    while True:
        # Capture the screen
        img = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Resize the frame
        frame = cv2.resize(frame, (frame_width, int(frame.shape[0] * (frame_width / frame.shape[1]))), interpolation=cv2.INTER_LINEAR)
        
        # Encode the frame as JPEG
        ret, jpeg_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
        
        # Check if JPEG encoding was successful
        if not ret:
            print("Error encoding frame as JPEG")
            continue
        
        # Serialize the JPEG-encoded frame
        data = pickle.dumps(jpeg_frame)
        
        # Send the serialized data over WebSocket
        await websocket.send(data)
        
        # Display the transmitting frame (same as the one being sent)
        cv2.imshow('TRANSMITTING SCREEN', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

async def main():
    # Increase max_size to 5 MB to allow higher quality frames
    async with websockets.serve(send_video, "localhost", 9999, max_size=5 * 10**6):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
