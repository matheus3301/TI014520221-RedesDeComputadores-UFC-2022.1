from enum import Enum


class Message(Enum):
    JOIN = "join"
    LEAVE = "leave"
    MEET = "meet"
    
    SKIP = "skip"
    ERROR = "error"
    ACK = "ack"
