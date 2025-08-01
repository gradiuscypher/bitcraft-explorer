import json
import logging
import os
from collections.abc import Generator
from pprint import pprint
from typing import Any

import httpx
from dotenv import load_dotenv, set_key
from websockets import Subprotocol
from websockets.sync.client import connect

logger = logging.getLogger(__name__)

load_dotenv()
BITCRAFT_EMAIL = os.getenv("BITCRAFT_EMAIL")
BITCRAFT_WSS_URL = os.getenv("BITCRAFT_WSS_URL")
BITCRAFT_TOKEN = os.getenv("BITCRAFT_TOKEN")

def save_to_env(key: str, value: str, env_file: str = ".env") -> None:
    """
    Alternative method using python-dotenv's set_key function.
    This preserves comments and formatting better.
    """
    success = set_key(env_file, key, value)
    if success:
        logger.info(f"Saved {key} to {env_file} using dotenv")
    else:
        logger.error(f"Failed to save {key} to {env_file}")


def get_bitcraft_token(save_token: bool = True) -> str | None:
    if BITCRAFT_TOKEN is not None:
        return BITCRAFT_TOKEN

    try:
        r = httpx.post(f"https://api.bitcraftonline.com/authentication/request-access-code?email={BITCRAFT_EMAIL}")
        code = input("Wait for an email and enter the code:")
        r = httpx.post(f"https://api.bitcraftonline.com/authentication/authenticate?email={BITCRAFT_EMAIL}&accessCode={code}")
        token_data = r.json()

        if save_token:
            save_to_env("BITCRAFT_TOKEN", token_data)

        return token_data

    except:
        logger.exception("Failed to get BitCraft token")
        return None


def get_user_id(username: str) -> dict | None:
    bc_token = get_bitcraft_token()
    if bc_token is None:
        logger.error("Failed to get BitCraft token")
        return None

    proto = Subprotocol("v1.json.spacetimedb")
    with connect(BITCRAFT_WSS_URL, additional_headers={"Authorization": "Bearer " + bc_token}, subprotocols=[proto], max_size=None, max_queue=None) as ws:
        ws.recv()
        sub = json.dumps(dict(Subscribe=dict(request_id=1, query_strings=[f"SELECT * FROM player_username_state where username='{username}'"])))
        ws.send(sub)
        for msg in ws:
            usernames = json.loads(msg)
            break
        ws.close()
    return usernames


def execute_query(query: str) -> dict | None:
    bc_token = get_bitcraft_token()
    if bc_token is None:
        logger.error("Failed to get BitCraft token")
        return None

    proto = Subprotocol("v1.json.spacetimedb")
    with connect(BITCRAFT_WSS_URL, additional_headers={"Authorization": "Bearer " + bc_token}, subprotocols=[proto], max_size=None, max_queue=None) as ws:
        ws.recv()
        sub = json.dumps(dict(Subscribe=dict(request_id=1, query_strings=[query])))
        ws.send(sub)
        for msg in ws:
            data = json.loads(msg)
            break
        ws.close()
    return data


def subscribe_to_query(query: str) -> None:
    bc_token = get_bitcraft_token()
    if bc_token is None:
        logger.error("Failed to get BitCraft token")
        return

    proto = Subprotocol("v1.json.spacetimedb")
    with connect(BITCRAFT_WSS_URL, additional_headers={"Authorization": "Bearer " + bc_token}, subprotocols=[proto], max_size=None, max_queue=None) as ws:
        ws.recv()
        sub = json.dumps(dict(Subscribe=dict(request_id=1, query_strings=[query])))
        ws.send(sub)
        try:
            for msg in ws:
                data = json.loads(msg)
                pprint(data)
        except KeyboardInterrupt:
            ws.close()
            return
        ws.close()


def subscribe_to_query_generator(query: str) -> Generator[Any, None, None]:
    """
    Generator version of subscribe_to_query that yields each websocket message.

    Usage:
        for message in subscribe_to_query_generator("SELECT * FROM player_state"):
            # Process each message
            print(message)
    """
    bc_token = get_bitcraft_token()
    if bc_token is None:
        logger.error("Failed to get BitCraft token")
        return

    proto = Subprotocol("v1.json.spacetimedb")
    with connect(BITCRAFT_WSS_URL, additional_headers={"Authorization": "Bearer " + bc_token}, subprotocols=[proto], max_size=None, max_queue=None) as ws:
        ws.recv()
        sub = json.dumps(dict(Subscribe=dict(request_id=1, query_strings=[query])))
        ws.send(sub)
        try:
            for msg in ws:
                data = json.loads(msg)
                yield data
        except KeyboardInterrupt:
            return
        finally:
            try:
                ws.close()
            except Exception:
                pass  # Connection might already be closed
