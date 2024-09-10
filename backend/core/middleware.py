from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send

class BaseMiddleware:
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def send_wrapper(message: Message) -> None:
            for scope_key in scope:
                # log.debug(f"scope key: {scope_key} value: {scope[scope_key]}")
                ...
            await send(message)
        await self.app(scope, receive, send_wrapper)


    async def send(
        self, message: Message, send: Send, request_headers: Headers
    ) -> None:

        if message["type"] != "http.response.start":
            await send(message)
            return
        await send(message)