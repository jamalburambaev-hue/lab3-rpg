from typing import Dict, List
from .game_event_type import GameEventType
from .game_event_listener import GameEventListener
from .game_event import GameEvent

class GameEventPublisher:
    def __init__(self):
        self._listeners: Dict[GameEventType, List[GameEventListener]] = {}

    def subscribe(self, event_type: GameEventType, listener: GameEventListener):
        self._listeners.setdefault(event_type, []).append(listener)

    def publish(self, event: GameEvent):
        for listener in self._listeners.get(event.type, []):
            listener.on_event(event)