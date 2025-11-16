pip install -e .      # ensure the project (and new package) is on PYTHONPATH
# Just inspect the prompt & ground-truth
python scripts/example/run_bfs_static.py --N 10 --p 0.25 --seed 42 --start 0 --dry_run
# Full run (uses repo's send_prompt() if configured)
python scripts/example/run_bfs_static.py --N 10 --p 0.25 --seed 42 --start 0 \
  --model gpt-4o --temperature 0.0 --max_tokens 128
