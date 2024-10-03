from aiogram import Router

# Функция подключения всех роутеров из handlers
def setup_router() -> Router:
    from . import other
    from . import redact
    router = Router()

    router.include_routers(
        other.router,
        redact.router
    )

    return router
