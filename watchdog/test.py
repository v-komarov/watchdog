"""
Модуль тестирования
"""
import argparse
import asyncio
import aiohttp
from settings import TOKEN, CHAT_ID
from telebot.async_telebot import AsyncTeleBot

tb = AsyncTeleBot(TOKEN)


async def send_message(msg):
    if msg:
        await tb.send_message(CHAT_ID, msg)


async def check_host(url):
    if url:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    print(resp.status)
            except aiohttp.ClientConnectorError as e:
                    print(e)


parser = argparse.ArgumentParser()
parser.add_argument('--msg', help='send message')
parser.add_argument('--url', help='check url')


if __name__ == "__main__":
    args = parser.parse_args()
    asyncio.run(check_host(args.url))
    asyncio.run(send_message(args.msg))
