import asyncio
import websockets
import pickle
import cv2

async def receive_video():
    async with websockets.connect("ws://localhost:9999") as websocket:
        while True:
            # Receive data from server
            data = await websocket.recv()
            
            # Deserialize the frame
            frame = pickle.loads(data)
            
            # Display the video (same as what the server transmits)
            cv2.imshow("RECEIVING VIDEO", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    asyncio.run(receive_video())
