# Multi-Agent Negotiation Simulation

A simulation-first codebase for studying autonomous negotiation behavior under explicit communication constraints, configurable reward functions, and reinforcement-learning-compatible environments.

## Scope

This project is intended as a research and prototyping baseline for:

- agent communication protocols
- reward-based bargaining
- episodic multi-agent simulation
- RL integration through Gymnasium and Stable-Baselines3
- agent-graph orchestration patterns inspired by LangGraph-style systems

## Repository Shape

```text
configs/                       # simulation presets and negotiation scenarios
experiments/                   # experiment notes and outputs
scripts/                       # runnable entry points
src/negotiation_lab/
  agents/                      # agent policies and stateful negotiators
  protocols/                   # message schema and turn-taking rules
  environment/                 # simulation environment and gym adapter
  rewards/                     # utility and reward shaping functions
  simulation/                  # orchestration and reporting
  rl/                          # Stable-Baselines integration points
  schemas/                     # typed simulation state
tests/                         # contract and behavior tests
```

## Core Idea

Each episode simulates a bargaining task between autonomous agents. Agents exchange structured messages, revise offers over time, and receive rewards based on agreement quality, efficiency, and adherence to reservation constraints.

The initial baseline uses deterministic policies so behavior is auditable. This makes it easier to evaluate reward shaping and communication mechanics before introducing learned policies.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
python scripts/run_simulation.py
pytest
```

## Next Research Steps

1. Train policy networks against the gym environment with PPO.
2. Add richer deal spaces with multiple issues and asymmetric information.
3. Integrate LLM-backed dialogue policies through LangGraph nodes.
4. Track emergent strategy metrics across repeated tournaments.
