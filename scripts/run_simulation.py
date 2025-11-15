from pathlib import Path

from negotiation_lab.simulation.runner import SimulationRunner


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    runner = SimulationRunner(project_root)
    outcome = runner.run_episode()
    print(outcome.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
