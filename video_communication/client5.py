import asyncio
import websockets
import cv2
import base64
import numpy as np

async def receive_video():
    uri = "ws://192.168.1.19:8765"  # Update with your server's address

    try:
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    # Receive base64 encoded frame from the server
                    base64_frame = await websocket.recv()
                    
                    # Decode the base64 frame
                    frame_data = base64.b64decode(base64_frame)
                    
                    # Convert to numpy array
                    frame_np = np.frombuffer(frame_data, np.uint8)
                    
                    # Decode the image from numpy array
                    frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
                    
                    # Display the frame using OpenCV
                    if frame is not None:
                        cv2.imshow("Receiving Video", frame)
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('q'):
                            break  # Exit on 'q' key press
                    else:
                        print("Received an empty frame.")

                except Exception as e:
                    print(f"Error receiving or processing frame: {str(e)}")
                    break

    except websockets.exceptions.ConnectionClosedError:
        print("Connection to the server closed.")
    except Exception as e:
        print(f"Error connecting to the server: {str(e)}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(receive_video())
