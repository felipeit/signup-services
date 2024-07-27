from typing import Protocol
from domain.event import Event


class FakeDispatcher:
    def send_events(self, *event: Event) -> None:
        for e in event:
            print(f"evento enviado: {e}")