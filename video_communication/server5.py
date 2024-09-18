import asyncio
import websockets
import cv2
import base64
import numpy as np

async def stream_video(websocket, path):
    video_source = 'E:/Videos/My iphone/video/IMG_0514.MP4'
    
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("Error: Couldn't open video source.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break  # Exit loop if no more frames are available

            # Resize frame if needed (optional)
            frame = cv2.resize(frame, (1280, 720))  # Resize to higher resolution, e.g., 1280x720

            # Encode the frame to JPEG format with higher quality
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]  # Set JPEG quality to 95
            _, buffer = cv2.imencode('.jpg', frame, encode_param)

            # Convert frame to base64
            base64_frame = base64.b64encode(buffer).decode('utf-8')

            # Send the base64 encoded frame via WebSocket
            await websocket.send(base64_frame)

            # Wait briefly before sending the next frame (adjust the delay to match the frame rate of the video)
            await asyncio.sleep(0.03)  # Approx. 30 FPS

    except websockets.exceptions.ConnectionClosedError:
        print("Client disconnected.")
    finally:
        cap.release()
        print("Video capture released.")

# Define server address and port
start_server = websockets.serve(stream_video, "0.0.0.0", 8765)

print("WebSocket server started.")

# Run the WebSocket server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
