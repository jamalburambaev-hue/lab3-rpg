from .game_event import GameEvent

class GameEventListener:
    def on_event(self, event: GameEvent) -> None:
        raise NotImplementedError