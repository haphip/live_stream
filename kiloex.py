import asyncio

from playwright.async_api import BrowserContext, expect
from loguru import logger

from data.models import Wallet
from data import config


kiloex_url = 'https://app.kiloex.io/trade'
airdrop_url = 'https://app.kiloex.io/airdrop'


async def connect_wallet(context: BrowserContext, wallet: Wallet):
    logger.info(f'{wallet.address} | Starting recover wallet')
    kiloex_page = context.pages[0]
    await kiloex_page.goto(kiloex_url)
    await kiloex_page.bring_to_front()

    await kiloex_page.wait_for_load_state()

    try:
        # окно "начать"
        # меняем на класс так как xpath постоянно меняется
        close_message_btn = kiloex_page.locator(
            '.arco-btn.arco-btn-primary.arco-btn-shape-square.arco-btn-size-large.arco-btn-status-normal.arco-btn-long'
        ).last
        await expect(close_message_btn.first).to_be_visible()
        await close_message_btn.click()
    except Exception:
        pass

    # ждем когда уйдут уведомления
    # await asyncio.sleep(2)

    # connect wallet
    connect_wallet_btn = kiloex_page.locator(
        # полный путь так как 2 id
        '//html/body/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button'
    )
    await expect(connect_wallet_btn.first).to_be_visible()
    await connect_wallet_btn.click()

    # mm_btn = kiloex_page.locator(
    #     '//html/body/div[17]/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div/button'
    # )
    mm_btn = kiloex_page.get_by_test_id('rk-wallet-button-metaMask').first
    await expect(mm_btn.first).to_be_visible()
    await mm_btn.click()

    await asyncio.sleep(config.DEFAULT_DELAY)

    mm_page = context.pages[-1]
    await mm_page.bring_to_front()

    # confirm connect
    await mm_page.get_by_test_id('confirm-btn').click()

    # confirm
    await mm_page.get_by_test_id('confirmation-submit-button').click()

    logger.success(f'Wallet {wallet.address} successfully connected to Kiloex')


async def change_chain(context: BrowserContext, wallet: Wallet):
    logger.info(f'{wallet.address} | Starting recover wallet')
    kiloex_page = context.pages[0]
    await kiloex_page.goto(kiloex_url)
    await kiloex_page.bring_to_front()

    await kiloex_page.wait_for_load_state()

    try:
        # close welcome gift
        # document.querySelectorAll('.arco-modal-close-btn')
        close_message_btn = kiloex_page.locator(
            '.arco-modal-close-btn'
        ).nth(3)
        await expect(close_message_btn.first).to_be_visible()
        await close_message_btn.click()
    except Exception:
        pass

    await kiloex_page.locator(
        '//html/body/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[2]/button'
    ).click()

    await kiloex_page.locator(
        '//html/body/div[8]/div/div[1]/div[2]/div/div/button[4]'
    ).click()

    await asyncio.sleep(config.DEFAULT_DELAY)

    mm_page = context.pages[-1]
    await mm_page.bring_to_front()

    await mm_page.get_by_test_id('confirmation-submit-button').click()

    await kiloex_page.bring_to_front()

    logger.success(f'Wallet {wallet.address} successfully change chain to BSC')


async def buy_eth(context: BrowserContext, wallet: Wallet, amount: float):
    for i in range(3):
        try:
            logger.info(f'{wallet.address} | Start buy ETH')
            kiloex_page = context.pages[0]
            await kiloex_page.goto(kiloex_url)
            await kiloex_page.bring_to_front()
            await kiloex_page.wait_for_load_state()

            await kiloex_page.locator(
                '//html/body/div[1]/div/div[1]/div/div/div/div/div/div/div/div[2]/div/section/div/section/main/div[2]/div/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div[2]/span/input'
            ).type(str(amount))

            await asyncio.sleep(config.DEFAULT_DELAY)

            place_order_btn = kiloex_page.locator(
                '//html/body/div[1]/div/div[1]/div/div/div/div/div/div/div/div[2]/div/section/div/section/main/div[2]/div/div[2]/div/div/div/div/div[3]/div[5]/div/button'
            )
            await expect(place_order_btn.first).to_be_enabled()
            await place_order_btn.first.click()

            await asyncio.sleep(config.DEFAULT_DELAY)

            mm_page = context.pages[-1]
            await mm_page.bring_to_front()

            await mm_page.get_by_test_id('confirm-footer-button').click()

            logger.success(f'Wallet {wallet.address} | Successfully swap {amount} USDT to ETH')
            return True
        except Exception as err:
            logger.error(f'({i}/3) {wallet.address} | {err}')


async def close_positions(context: BrowserContext, wallet: Wallet):
    logger.info(f'{wallet.address} | Starting close positions')
    kiloex_page = context.pages[0]
    await kiloex_page.goto(kiloex_url)
    await kiloex_page.bring_to_front()

    # закрыть позиции
    await kiloex_page.locator('.closeall').first.click()

    # подтвердить
    await kiloex_page.locator(
        '.arco-btn.arco-btn-primary.arco-btn-shape-square.arco-btn-size-large.arco-btn-status-normal.arco-btn-long'
    ).first.click()

    await asyncio.sleep(config.DEFAULT_DELAY)

    mm_page = context.pages[-1]
    await mm_page.bring_to_front()

    # confirm
    await mm_page.get_by_test_id('confirm-footer-button').click()

    await kiloex_page.bring_to_front()

    logger.success(f'Wallet {wallet.address} successfully close all positions ETH')


async def check_airdrop(context: BrowserContext, wallet: Wallet):
    logger.info(f'{wallet.address} | Start checking airdrop')
    kiloex_page = context.pages[0]
    await kiloex_page.goto(airdrop_url)
    await kiloex_page.bring_to_front()

    # .arco-btn.arco-btn-primary.arco-btn-shape-square.arco-btn-size-large.arco-btn-status-normal
    await kiloex_page.locator(
        '.arco-btn.arco-btn-primary.arco-btn-shape-square.arco-btn-size-large.arco-btn-status-normal'
    ).first.click()

    await asyncio.sleep(config.DEFAULT_DELAY)

    mm_page = context.pages[-1]
    await mm_page.bring_to_front()

    # confirm
    await mm_page.get_by_test_id('confirm-footer-button').click()

    await kiloex_page.bring_to_front()

    airdrop_points_row = kiloex_page.locator('//*[@id="myPoint"]/div[2]/div/div[1]/h2').first
    await expect(airdrop_points_row).to_be_visible()
    airdrop_points = await airdrop_points_row.inner_text()
    logger.success(f'Wallet {wallet.address} successfully get airdrop points: {airdrop_points}')
