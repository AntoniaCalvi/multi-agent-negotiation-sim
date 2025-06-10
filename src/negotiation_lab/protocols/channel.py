from negotiation_lab.schemas.state import NegotiationMessage


class CommunicationChannel:
    def __init__(self) -> None:
        self._messages: list[NegotiationMessage] = []

    def publish(self, message: NegotiationMessage) -> None:
        self._messages.append(message)

    def history(self) -> list[NegotiationMessage]:
        return list(self._messages)

    def messages_for(self, recipient: str) -> list[NegotiationMessage]:
        return [message for message in self._messages if message.recipient == recipient]
