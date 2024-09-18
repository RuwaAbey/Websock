import asyncio
import websockets
import cv2
import numpy as np
import base64

# Define the path to the video file
video_path = 'E:\\Videos\\My iphone\\IMG_4854.MP4'  # Update this path to your video file

# Define the scale factor for enlarging the frames
scale_factor = 2.0  # Change this value to enlarge the video (e.g., 2.0 for doubling the size)

async def stream_video(websocket, path):
    print("Client connected.")
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    while True:
        try:
            # Read a frame from the video
            ret, frame = cap.read()
            
            if not ret:
                print("End of video stream or error.")
                break

            # Resize the frame to a higher resolution first (if needed)
            frame = cv2.resize(frame, (640, int(640 * frame.shape[0] / frame.shape[1])), interpolation=cv2.INTER_CUBIC)

            # Enlarge the frame using high-quality resampling
            frame = cv2.resize(frame, 
                               (int(frame.shape[1] * scale_factor), 
                                int(frame.shape[0] * scale_factor)), 
                               interpolation=cv2.INTER_CUBIC)  # Use cubic interpolation

            # Encode the frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)

            # Convert the frame to base64
            base64_frame = base64.b64encode(buffer).decode('utf-8')

            # Send the base64 encoded frame via WebSocket
            await websocket.send(base64_frame)

            # Display the transmitting video
            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        except websockets.exceptions.ConnectionClosedError:
            print("Client disconnected.")
            break
        except Exception as e:
            print(f"Error during transmission: {str(e)}")
            break

    cap.release()
    cv2.destroyAllWindows()

# Define server address and port
async def main():
    server = await websockets.serve(stream_video, "0.0.0.0", 8765)  # Listen on all interfaces on port 8765
    print("WebSocket server started.")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
