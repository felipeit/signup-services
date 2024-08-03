import asyncio
from dataclasses import asdict
from typing import Any, Optional

import aiormq
from aiormq.abc import AbstractChannel, DeliveredMessage

from domain.event import Event

# from domain.event import Event

# async def main():
#     global MESSAGE
#     body = b"Hello World!"
#     # Perform connection
#     connection = await aiormq.connect("amqp://guest:guest@localhost//")
#     # Creating a channel
#     channel = await connection.channel()
#     declare_ok = await channel.queue_declare("user-registered", auto_delete=False)
#     # Sending the message
#     await channel.basic_publish(
#         body,
#         exchange="user-registered-ex",
#         routing_key="signup.email",
#     )
#     print(f" [x] Sent {body}")
#     await channel.basic_get(declare_ok.queue)
#     print(f" [x] Received message from {declare_ok.queue!r}")


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


class RabbitMQDispatcher:
    def __init__(self, con_string: str = "amqp://guest:guest@localhost//") -> None:
        self.con_string = con_string
        self._channel: AbstractChannel | None = None

    async def send_events(self, *event: Event) -> None:
        await self.__get_connection()
        for e in event:
            # await self._channel.queue_declare(e.identifier, auto_delete=False)
            await self._channel.basic_publish(
                body=bytes(e),
                routing_key=e.identifier,  # user-registered
                exchange="user-registered",  # user-registered se for um signup
            )

    async def __get_connection(self) -> AbstractChannel:
        if not self._channel:
            connection = await aiormq.connect(self.con_string)
            self._channel = await connection.channel()
        return self._channel
