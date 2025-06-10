from pathlib import Path

import orjson
import pandas as pd

from negotiation_lab.environment.negotiation_env import NegotiationEnv
from negotiation_lab.schemas.state import AgentProfile, NegotiationOutcome


class SimulationRunner:
    def __init__(self, project_root: Path) -> None:
        self._project_root = project_root

    def load_baseline_agents(self) -> tuple[AgentProfile, AgentProfile, str]:
        payload = orjson.loads(
            (self._project_root / "configs" / "baseline_scenario.json").read_bytes()
        )
        buyer = AgentProfile(
            agent_id="buyer-1",
            role="buyer",
            target_price=payload["buyer_target_price"],
            reservation_price=payload["buyer_reservation_price"],
            concession_rate=0.05,
        )
        seller = AgentProfile(
            agent_id="seller-1",
            role="seller",
            target_price=payload["seller_target_price"],
            reservation_price=payload["seller_reservation_price"],
            concession_rate=0.05,
        )
        return buyer, seller, payload["issue"]

    def run_episode(self) -> NegotiationOutcome:
        buyer, seller, issue = self.load_baseline_agents()
        env = NegotiationEnv(buyer=buyer, seller=seller, issue=issue)
        observation, _ = env.reset()
        done = False
        info = {}

        while not done:
            action = 0
            observation, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

        del observation, reward
        return info["outcome"]

    def tournament(self, episodes: int = 5) -> pd.DataFrame:
        rows: list[dict[str, object]] = []
        for episode_id in range(episodes):
            outcome = self.run_episode()
            rows.append(
                {
                    "episode_id": episode_id,
                    "agreement_reached": outcome.agreement_reached,
                    "final_price": outcome.final_price,
                    "rounds_used": outcome.rounds_used,
                    "buyer_reward": outcome.buyer_reward,
                    "seller_reward": outcome.seller_reward,
                }
            )
        return pd.DataFrame(rows)
