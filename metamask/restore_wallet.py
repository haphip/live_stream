from playwright.async_api import BrowserContext

from loguru import logger

from data.models import Wallet
from data import config


async def restore_wallet(context: BrowserContext, wallet: Wallet) -> bool:
    # todo: добавить попытки
    try:
        logger.info(f'{wallet.address} | Starting recover wallet')
        page = context.pages[0]
        await page.goto(f'chrome-extension://{config.MM_EXTENTION_IDENTIFIER}/home.html#onboarding/welcome')
        await page.bring_to_front()

        await page.wait_for_load_state()

        # Agree checkbox
        await page.get_by_test_id('onboarding-terms-checkbox').click()

        # import wallet btn
        await page.get_by_test_id('onboarding-import-wallet').click()

        # no, thanks
        await page.get_by_test_id('metametrics-no-thanks').click()

        # fill seed phrase
        for i, word in zip(range(12), config.MM_SEED.split()):
            await page.locator(f'//*[@id="import-srp__srp-word-{i}"]').fill(word)

        # confirm secret phrase
        await page.get_by_test_id('import-srp-confirm').click()

        # fill password
        await page.get_by_test_id('create-password-new').fill(config.MM_EXTENTION_PASSWORD)
        await page.get_by_test_id('create-password-confirm').fill(config.MM_EXTENTION_PASSWORD)

        # agree checkbox
        await page.get_by_test_id('create-password-terms').click()

        # import wallet btn
        await page.get_by_test_id('create-password-import').click()

        # done
        await page.get_by_test_id('onboarding-complete-done').click()

        # next
        await page.get_by_test_id('pin-extension-next').click()

        # done
        await page.get_by_test_id('pin-extension-done').click()

        logger.success(f'{wallet.address} | Wallet Ready To Work')
        # await page.close()
        return True

    except Exception as err:
        logger.error(f'{wallet.address} | Not Recovered ({err})')
        logger.info(f'Error when getting an account, trying again')

    return False
