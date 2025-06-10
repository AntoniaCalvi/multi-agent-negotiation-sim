import gymnasium as gym
import numpy as np
from gymnasium import spaces

from negotiation_lab.agents.policies import RuleBasedNegotiationAgent
from negotiation_lab.protocols.channel import CommunicationChannel
from negotiation_lab.rewards.utility import RewardModel
from negotiation_lab.schemas.state import (
    AgentProfile,
    MessageType,
    NegotiationOutcome,
    NegotiationState,
)
from negotiation_lab.settings import get_settings


class NegotiationEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        buyer: AgentProfile,
        seller: AgentProfile,
        issue: str = "generic-deal",
    ) -> None:
        super().__init__()
        settings = get_settings()
        self.buyer = buyer
        self.seller = seller
        self.issue = issue
        self.max_rounds = settings.simulation_max_rounds
        self.reward_model = RewardModel(settings.default_discount_factor)
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(4,), dtype=np.float32)
        self.action_space = spaces.Discrete(3)
        self._buyer_agent = RuleBasedNegotiationAgent(buyer)
        self._seller_agent = RuleBasedNegotiationAgent(seller)
        self._channel = CommunicationChannel()
        self.state = NegotiationState(issue=issue, max_rounds=self.max_rounds)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self._channel = CommunicationChannel()
        self.state = NegotiationState(issue=self.issue, max_rounds=self.max_rounds)
        return self._observe(), {}

    def step(self, action: int):
        del action
        buyer_message = self._buyer_agent.act(self.state, self.seller.agent_id)
        self._record_message(buyer_message)

        if buyer_message.kind == MessageType.WITHDRAW:
            return self._terminal_transition(False, None)

        if buyer_message.offer_value is not None:
            self.state.active_offer = buyer_message.offer_value

        seller_message = self._seller_agent.act(self.state, self.buyer.agent_id)
        self._record_message(seller_message)

        if seller_message.kind == MessageType.ACCEPT:
            self.state.accepted = True
            return self._terminal_transition(True, self.state.active_offer)

        if seller_message.kind == MessageType.WITHDRAW:
            return self._terminal_transition(False, None)

        if seller_message.offer_value is not None:
            self.state.active_offer = seller_message.offer_value

        self.state.round_index += 1
        truncated = self.state.round_index >= self.state.max_rounds
        if truncated:
            return self._terminal_transition(False, None, truncated=True)

        return self._observe(), 0.0, False, False, {"transcript": self.state.transcript}

    def _record_message(self, message) -> None:
        self._channel.publish(message)
        self.state.transcript.append(message)

    def _observe(self):
        active_offer = self.state.active_offer or 0.0
        return np.array(
            [
                self.state.round_index / self.state.max_rounds,
                active_offer,
                self.buyer.reservation_price,
                self.seller.reservation_price,
            ],
            dtype=np.float32,
        )

    def _terminal_transition(
        self,
        agreement_reached: bool,
        final_price: float | None,
        truncated: bool = False,
    ):
        outcome = NegotiationOutcome(
            agreement_reached=agreement_reached,
            final_price=final_price,
            rounds_used=self.state.round_index + 1,
            buyer_reward=0.0,
            seller_reward=0.0,
            transcript=self.state.transcript,
        )
        buyer_reward, seller_reward = self.reward_model.score(outcome, self.buyer, self.seller)
        outcome.buyer_reward = buyer_reward
        outcome.seller_reward = seller_reward
        info = {"outcome": outcome, "transcript": self.state.transcript}
        return self._observe(), buyer_reward + seller_reward, True, truncated, info
