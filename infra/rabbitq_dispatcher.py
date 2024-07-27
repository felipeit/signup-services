from dataclasses import asdict
from typing import Any
from domain.event import Event
import aiormq


class RabbitMQDispatcher:
    def __init__(self) -> None:
        self._channel = self.__get_connection()

    def send_events(self, *event: Event) -> None:
        for e in event:
             self._channel.channel.queue_declare(e.identifier, auto_delete=True)
             self._channel.basic_publish(asdict(e), routing_key=e.identifier)

    def __get_connection(self) -> Any:
        connection = aiormq.connect("amqp://guest:guest@localhost//")
        channel = connection.channel()
        return channel