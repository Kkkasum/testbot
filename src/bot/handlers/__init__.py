from aiogram import Dispatcher

from ._main import router as main_router


def include_routers(dp: Dispatcher):
    dp.include_router(main_router)
