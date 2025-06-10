from negotiation_lab.schemas.state import (
    AgentProfile,
    MessageType,
    NegotiationMessage,
    NegotiationState,
)


class RuleBasedNegotiationAgent:
    def __init__(self, profile: AgentProfile) -> None:
        self.profile = profile

    def act(self, state: NegotiationState, counterpart_id: str) -> NegotiationMessage:
        if state.active_offer is None:
            offer = self._opening_offer()
            return self._offer_message(state, counterpart_id, offer)

        if self._is_acceptable(state.active_offer):
            return NegotiationMessage(
                sender=self.profile.agent_id,
                recipient=counterpart_id,
                kind=MessageType.ACCEPT,
                content="Offer accepted.",
                offer_value=state.active_offer,
                round_index=state.round_index,
            )

        next_offer = self._counter_offer(state.active_offer)
        if next_offer is None:
            return NegotiationMessage(
                sender=self.profile.agent_id,
                recipient=counterpart_id,
                kind=MessageType.WITHDRAW,
                content="No mutually beneficial deal remains under current constraints.",
                round_index=state.round_index,
            )

        return self._offer_message(state, counterpart_id, next_offer)

    def _opening_offer(self) -> float:
        return round(self.profile.target_price, 3)

    def _is_acceptable(self, offer_value: float) -> bool:
        if self.profile.role == "buyer":
            return offer_value <= self.profile.reservation_price
        return offer_value >= self.profile.reservation_price

    def _counter_offer(self, current_offer: float) -> float | None:
        if self.profile.role == "buyer":
            next_offer = current_offer - self.profile.concession_rate
            if next_offer < self.profile.target_price:
                next_offer = self.profile.target_price
            return round(next_offer, 3) if next_offer <= self.profile.reservation_price else None

        next_offer = current_offer + self.profile.concession_rate
        if next_offer > self.profile.target_price:
            next_offer = self.profile.target_price
        return round(next_offer, 3) if next_offer >= self.profile.reservation_price else None

    def _offer_message(
        self,
        state: NegotiationState,
        counterpart_id: str,
        offer_value: float,
    ) -> NegotiationMessage:
        return NegotiationMessage(
            sender=self.profile.agent_id,
            recipient=counterpart_id,
            kind=MessageType.OFFER,
            content=f"Proposed settlement at {offer_value:.3f}.",
            offer_value=offer_value,
            round_index=state.round_index,
        )
