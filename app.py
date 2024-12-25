import asyncio

from playwright.async_api import async_playwright
from loguru import logger

import utils
import kiloex
from data import config
from metamask.restore_wallet import restore_wallet
from data.wallets import WALLETS


async def process_wallet(wallet):
    async with async_playwright() as p:
        if config.PROXY:
            proxy = await utils.format_proxy(config.PROXY)

        args: list = [
            f"--disable-extensions-except={config.MM_EXTENTION_PATH}",
            f"--load-extension={config.MM_EXTENTION_PATH}"
        ]
        if config.HEADLESS:
            args.append(f"--headless=new")

        context = await p.chromium.launch_persistent_context(
            '',
            headless=False,
            args=args,
            proxy=proxy,
            slow_mo=config.SLOW_MO
        )
        await asyncio.sleep(2)
        if not await restore_wallet(context=context, wallet=wallet):
            logger.error(f'{wallet.address}: Can not restore wallet')
            return
        await asyncio.sleep(3)

        logger.success('Start work')

        await kiloex.connect_wallet(context=context, wallet=wallet)
        await kiloex.change_chain(context=context, wallet=wallet)
        await kiloex.buy_eth(context=context, wallet=wallet, amount=20)
        await asyncio.sleep(20)
        await kiloex.close_positions(context=context, wallet=wallet)
        await asyncio.sleep(20)
        await kiloex.check_airdrop(context=context, wallet=wallet)

        await asyncio.sleep(999)


async def main():
    await process_wallet(wallet=WALLETS[0])


if __name__ == '__main__':
    asyncio.run(main())
