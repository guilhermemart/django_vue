import asyncio
import base64
import os
import websockets

async def receiver(websocket):
    async for message in websocket:
        output_picture = open(os.path.join(os.path.expanduser("~"), "media", "continuous", 'output_img.png'), 'wb')
        output_picture.write(base64.decodebytes(message))
        output_picture.close()


async def main():
    async with websockets.serve(receiver, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())