import asyncio
import websockets
import pickle
import cv2

async def receive_video():
    async with websockets.connect("ws://localhost:9999") as websocket:
        while True:
            # Receive data from server
            data = await websocket.recv()
            
            # Deserialize the JPEG-encoded frame
            jpeg_frame = pickle.loads(data)
            
            # Decode the JPEG-encoded frame
            frame = cv2.imdecode(jpeg_frame, cv2.IMREAD_COLOR)
            
            # Display the video
            cv2.imshow("RECEIVING VIDEO", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    asyncio.run(receive_video())
