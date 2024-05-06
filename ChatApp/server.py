import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        print(f"message from client: {message}")
        await websocket.send(f"Hi Client, Your message is {message}")

start_server=websockets.serve(echo, 'localhost', 6534)

try:
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except Exception as e:
    print(f"server stopped due to: {e}") 
except KeyboardInterrupt as  e:
    print(f"server stopped due to: KeyBoardInterrupt")
