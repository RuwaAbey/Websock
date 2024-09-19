import asyncio
import websockets
import cv2
import base64

video_path = r'C:\Users\Pasindu\Downloads\video.mp4'

async def upload_video():
    uri = "ws://13.60.222.225:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server.")
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Error: Unable to open video file at {video_path}")
                return
            
            print("Start reading, displaying, and sending video frames.")
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("End of video stream or error reading frame.")
                    break
                
                # Show the current video frame in a window
                cv2.imshow('Transmitting Video', frame)
                
                # Break if 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Video transmission stopped by user.")
                    break

                # Encode frame to JPEG and base64
                _, buffer = cv2.imencode('.jpg', frame)
                if buffer is None:
                    print("Error: Frame encoding failed.")
                    continue
                
                base64_frame = base64.b64encode(buffer).decode('utf-8')
                
                try:
                    # Send the base64-encoded frame to the server
                    await websocket.send(base64_frame)
                    print("Frame sent to server.")
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"Error sending frame: {e}")
                    break
                except Exception as e:
                    print(f"Error sending frame: {e}")
                
                await asyncio.sleep(0.03)  # Delay to simulate video frame rate (30 FPS)
            
            cap.release()
            cv2.destroyAllWindows()  # Close the video window
            print("Video capture released.")
    
    except websockets.exceptions.ConnectionClosed as e:
        print(f"WebSocket connection closed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if _name_ == "_main_":
    asyncio.run(upload_video())