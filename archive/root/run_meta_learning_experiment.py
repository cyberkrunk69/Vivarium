import argparse
import json
import os
import random
import numpy as np

# Assume existing meta_learner module provides a MetaLearner class
from meta_learner import MetaLearner

def main():
    parser = argparse.ArgumentParser(description="Run meta‑learning comparison experiment")
    parser.add_argument("--variant", choices=["fixed", "adaptive"], required=True,
                        help="Choose the learning strategy variant")
    args = parser.parse_args()

    # Set deterministic seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Instantiate the learner
    learner = MetaLearner(variant=args.variant)

    # Run a fixed number of meta‑learning iterations
    history = learner.run_meta_training(iterations=20)

    # Save results
    os.makedirs("experiments/meta_learning_comparison/results", exist_ok=True)
    out_path = f"experiments/meta_learning_comparison/results/{args.variant}.json"
    with open(out_path, "w") as f:
        json.dump(history, f, indent=2)

    print(f"Results saved to {out_path}")

if __name__ == "__main__":
    main()