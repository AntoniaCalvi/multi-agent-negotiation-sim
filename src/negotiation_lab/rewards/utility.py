from negotiation_lab.schemas.state import AgentProfile, NegotiationOutcome


class RewardModel:
    def __init__(self, discount_factor: float = 0.95) -> None:
        self._discount_factor = discount_factor

    def score(
        self,
        outcome: NegotiationOutcome,
        buyer: AgentProfile,
        seller: AgentProfile,
    ) -> tuple[float, float]:
        if not outcome.agreement_reached or outcome.final_price is None:
            return -1.0, -1.0

        buyer_surplus = max(0.0, buyer.reservation_price - outcome.final_price)
        seller_surplus = max(0.0, outcome.final_price - seller.reservation_price)
        efficiency_penalty = self._discount_factor ** max(outcome.rounds_used - 1, 0)

        return round(buyer_surplus * efficiency_penalty, 4), round(
            seller_surplus * efficiency_penalty,
            4,
        )
