from dataclasses import dataclass


@dataclass
class Event:
    event: str
    time: float


@dataclass
class SpeechEvent(Event):
    query: str
