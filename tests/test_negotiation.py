from pathlib import Path

from negotiation_lab.rewards.utility import RewardModel
from negotiation_lab.schemas.state import AgentProfile, NegotiationOutcome
from negotiation_lab.simulation.runner import SimulationRunner

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_reward_model_returns_negative_reward_without_agreement() -> None:
    buyer = AgentProfile(
        agent_id="buyer-test",
        role="buyer",
        target_price=0.5,
        reservation_price=0.7,
        concession_rate=0.05,
    )
    seller = AgentProfile(
        agent_id="seller-test",
        role="seller",
        target_price=0.8,
        reservation_price=0.45,
        concession_rate=0.05,
    )
    outcome = NegotiationOutcome(
        agreement_reached=False,
        final_price=None,
        rounds_used=8,
        buyer_reward=0.0,
        seller_reward=0.0,
        transcript=[],
    )

    buyer_reward, seller_reward = RewardModel().score(outcome, buyer, seller)

    assert buyer_reward == -1.0
    assert seller_reward == -1.0


def test_simulation_runner_returns_outcome() -> None:
    runner = SimulationRunner(PROJECT_ROOT)

    outcome = runner.run_episode()

    assert outcome.rounds_used >= 1
    assert isinstance(outcome.agreement_reached, bool)
