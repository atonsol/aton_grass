#script for 1 user_id and a whole bunch of proxies
import asyncio
import random
import ssl
import json
import time
import uuid
import requests
import shutil
from loguru import logger
from websockets_proxy import Proxy, proxy_connect
from fake_useragent import UserAgent

user_agent = UserAgent(os=['windows', 'macos', 'linux'], browsers='chrome')
random_user_agent = user_agent.random

async def connect_to_wss(socks5_proxy, user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy))
    logger.info(f"Connecting with Device ID: {device_id}")
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": random_user_agent,
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            urilist = ["wss://proxy2.wynd.network:4444/","wss://proxy2.wynd.network:4650/"]
            uri = random.choice(urilist)
            #uri = "wss://proxy.wynd.network:4650/"
            server_hostname = "proxy2.wynd.network"
            proxy = Proxy.from_url(socks5_proxy)
            async with proxy_connect(uri, proxy=proxy, ssl=ssl_context, server_hostname=server_hostname,
                                     extra_headers=custom_headers) as websocket:
                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        logger.debug(f"Sending PING: {send_message}")
                        await websocket.send(send_message)
                        await asyncio.sleep(5)
                # asyncio.create_task(send_http_request_every_10_seconds(socks5_proxy, device_id))
                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(f"Received message: {message}")
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "desktop",
                                "version": "4.29.0",
                            }
                        }
                        logger.debug(f"Sending AUTH response: {auth_response}")
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(f"Sending PONG response: {pong_response}")
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(f"Error with proxy {socks5_proxy}: {e}")


async def main():
    #find user_id on the site in conlose localStorage.getItem('userId') (if you can't get it, write allow pasting)
    #user_ids
    with open('usergrass.txt', 'r') as file:
            user_ids = file.read().splitlines()
        
    with open('proxy_list.txt', 'r') as file:
            local_proxies = file.read().splitlines()
        
    tasks = [asyncio.ensure_future(connect_to_wss(i, user_ids)) for i in local_proxies]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    #letsgo
    asyncio.run(main())