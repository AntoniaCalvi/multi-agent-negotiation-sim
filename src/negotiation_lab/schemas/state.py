from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field


class MessageType(StrEnum):
    OFFER = "offer"
    ACCEPT = "accept"
    REJECT = "reject"
    WITHDRAW = "withdraw"
    INFO = "info"


class NegotiationMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    sender: str
    recipient: str
    kind: MessageType
    content: str
    offer_value: float | None = Field(default=None, ge=0.0, le=1.0)
    round_index: int = Field(ge=0)


class AgentProfile(BaseModel):
    agent_id: str
    role: str
    target_price: float = Field(ge=0.0, le=1.0)
    reservation_price: float = Field(ge=0.0, le=1.0)
    concession_rate: float = Field(gt=0.0, le=1.0)


class NegotiationState(BaseModel):
    issue: str
    round_index: int = Field(default=0, ge=0)
    max_rounds: int = Field(gt=0)
    active_offer: float | None = Field(default=None, ge=0.0, le=1.0)
    accepted: bool = False
    transcript: list[NegotiationMessage] = Field(default_factory=list)


class NegotiationOutcome(BaseModel):
    agreement_reached: bool
    final_price: float | None = None
    rounds_used: int
    buyer_reward: float
    seller_reward: float
    transcript: list[NegotiationMessage]
