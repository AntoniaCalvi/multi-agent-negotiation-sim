from stable_baselines3 import PPO

from negotiation_lab.environment.negotiation_env import NegotiationEnv


class StableBaselinesTrainer:
    def __init__(self, env: NegotiationEnv) -> None:
        self._env = env

    def build_model(self) -> PPO:
        return PPO("MlpPolicy", self._env, verbose=0)
