#!/usr/bin/env python3
"""
Run a single static-graph BFS instance end-to-end:
  - Generate G(N, p) graph (undirected, 0-indexed)
  - Build prompt with EXACT instruction:
        "Generate the Breath First Search traversal of this graph"
  - Send to model using the repo's API helper (if available)
  - Print metrics
"""
import argparse
from static_bfs.static_data import StaticGraphGenER
from static_bfs.bfs_task import BFSOrderTask
from static_bfs.static_prompt import StaticGraphPrompt

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--N", type=int, default=10)
    p.add_argument("--p", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--start", type=int, default=0)
    # model args (reuse repo API if present)
    p.add_argument("--model", type=str, default="gpt-4o")
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--max_tokens", type=int, default=128)
    p.add_argument("--api_base", type=str, default=None)
    p.add_argument("--api_key", type=str, default=None)
    p.add_argument("--dry_run", action="store_true",
                   help="Do not call model; just print prompt and GT answer.")
    return p.parse_args()

def maybe_send_prompt(prompt_text, args):
    """
    Uses the repo's API helper if available; otherwise returns None.
    """
    #try:
    from llm4dyg.utils.api import send_prompt
    return send_prompt(
            args.model,
            prompt_text,
            temperature=args.temperature,
            max_tokens=args.max_tokens)
            #api_base=args.api_base,
            #api_key=args.api_key)
    #except Exception as e:
    #    print(f"[warn] Could not send prompt via repo API: {e}")
    #    return None

def main():
    args = parse_args()
    gen = StaticGraphGenER()
    task = BFSOrderTask(start=args.start)
    prompter = StaticGraphPrompt(task, args=args)

    info = gen.sample_graph(N=args.N, p=args.p, seed=args.seed)
    qa = task.generate_qa(info)
    prompt_qa = prompter.generate_prompt_qa(**qa)

    print("=== PROMPT ===")
    print(prompt_qa['prompt'])
    print("\n=== GROUND TRUTH ANSWER ===")
    print(qa['answer'])

    if args.dry_run:
        return

    model_output = maybe_send_prompt(prompt_qa['prompt'], args)
    print("\n=== MODEL RAW OUTPUT ===")
    print(model_output)

    metrics = task.evaluate(qa, model_output)
    print("\n=== METRICS ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()

