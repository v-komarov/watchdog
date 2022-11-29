import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from telebot.async_telebot import AsyncTeleBot

from data import hosts
from settings import TOKEN, CHAT_ID, CHECK_BOT_SEC, CHECK_SITE_SEC


tb = AsyncTeleBot(TOKEN)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger()

first_date = datetime(1970, 1, 1)
checking_log = {}


async def bot_alive():
    """Проверка сервиса"""
    while True:
        msg = "I'm alive."
        await tb.send_message(CHAT_ID, msg)
        logger.info(msg)
        await asyncio.sleep(CHECK_BOT_SEC)


async def check_site(hosts):
    """Проверка опроса сайтов"""
    while True:
        await asyncio.sleep(CHECK_SITE_SEC)
        for host in hosts:
            if checking_log.get(host.host, first_date) < datetime.now() - timedelta(minutes=30):
                msg = "{} Has a problem.".format(host.host)
                await tb.send_message(CHAT_ID, msg)
                logger.critical(msg)


async def connect_error(host):
    """Нет связи"""
    msg = "{} Couldn't connect.".format(host.host)
    if host.check_error >= host.check_times:
        await tb.send_message(CHAT_ID, msg)
        logger.critical(msg)
    else:
        logger.error(msg)


async def content_error(host):
    """Нет искомого контента на странице"""
    msg = "{} Couldn't get content.".format(host.host)
    if host.check_error >= host.check_times:
        await tb.send_message(CHAT_ID, msg)
        logger.critical(msg)
    else:
        logger.error(msg)


async def status_error(host, resp):
    """Код статуса ответа не 200"""
    msg = "{} status_code: {}".format(
        host.host, resp.status
    )
    if host.check_error >= host.check_times:
        await tb.send_message(CHAT_ID, msg)
        logger.critical(msg)
    else:
        logger.error(msg)


async def checking(host):
    """Проверка хостов"""
    async with aiohttp.ClientSession() as session:
        while True:

            try:
                resp = await asyncio.wait_for(session.get(host.host), timeout=5.0)
                if resp.status == 200:
                    """Проверка содержимого сайта"""
                    body = await resp.text()
                    if body.find(host.check_text) == -1:
                        host.check_error += 1
                        await content_error(host)
                    else:
                        logger.info("{} OK.".format(host.host))
                        host.check_error = 0
                else:
                    host.check_error += 1
                    await status_error(host, resp)

            except (aiohttp.ClientConnectorError, asyncio.TimeoutError, aiohttp.ClientError):
                host.check_error += 1
                await connect_error(host)

            checking_log[host.host] = datetime.now()
            await asyncio.sleep(host.check_period_sec)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(checking(host)) for host in hosts()]
    tasks.append(loop.create_task(bot_alive()))
    tasks.append(loop.create_task(check_site(hosts())))
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
