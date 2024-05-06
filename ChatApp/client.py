import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://localhost:6534") as websocket:
        message=input("Enter message to be sent to server")
        await websocket.send(message)
        response = await websocket.recv()
        print(f"server sent: {response}")

asyncio.get_event_loop().run_until_complete(hello())