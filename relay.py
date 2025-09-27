import asyncio, websockets
LOCAL="127.0.0.1"; LPORT=38280
REMOTE="wss://ap.jalchavware.com:38281"

async def pump(src, dst):
    try:
        async for msg in src: await dst.send(msg)
    finally:
        try: await dst.close()
        except: pass

async def handler(ws, path):
    async with websockets.connect(REMOTE, ping_interval=20, ping_timeout=60) as remote:
        await asyncio.gather(pump(ws, remote), pump(remote, ws))

async def main():
    async with websockets.serve(handler, LOCAL, LPORT): await asyncio.Future()

asyncio.run(main())