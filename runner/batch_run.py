#!/usr/bin/env python3

import argparse
import glob
import os
import subprocess
import sys
import time


FRAMEWORKS = ["langgraph", "crewai", "autogen"]


def get_tasks(start=None, end=None):
    """Return benchmark task JSON files, sorted by task number."""

    files = glob.glob(os.path.join("tasks", "t*.json"))

    task_files = []

    for path in files:
        filename = os.path.basename(path)

        # Only include files like t01.json, t02.json, etc.
        if not filename.startswith("t"):
            continue

        task_id = filename[:-5]

        if not task_id[1:].isdigit():
            continue

        number = int(task_id[1:])

        if start is not None and number < start:
            continue

        if end is not None and number > end:
            continue

        task_files.append((number, path))

    task_files.sort(key=lambda x: x[0])

    return [path for _, path in task_files]


def main():
    parser = argparse.ArgumentParser(
        description="Run benchmark tasks across all frameworks."
    )

    parser.add_argument(
        "--start",
        type=int,
        default=None,
        help="First task number to run",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="Last task number to run",
    )

    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="Number of repeats for each task/framework combination",
    )

    parser.add_argument(
        "--frameworks",
        nargs="+",
        choices=FRAMEWORKS,
        default=FRAMEWORKS,
        help="Frameworks to run",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="Per-run timeout in seconds (default: 180)",
    )

    args = parser.parse_args()

    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )

    os.chdir(project_root)

    tasks = get_tasks(args.start, args.end)

    if not tasks:
        print("ERROR: No task files found.")
        return 1

    total_runs = len(tasks) * len(args.frameworks) * args.repeats

    print("=" * 70)
    print("BATCH BENCHMARK RUNNER")
    print("=" * 70)
    print(f"Tasks:      {len(tasks)}")
    print(f"Frameworks: {', '.join(args.frameworks)}")
    print(f"Repeats:    {args.repeats}")
    print(f"Total runs: {total_runs}")
    print(f"Timeout:    {args.timeout}s per run")
    print("=" * 70)

    completed = 0
    passed = 0
    failed = 0
    crashed = 0
    timed_out = 0

    overall_start = time.time()

    for task_path in tasks:

        task_name = os.path.basename(task_path).replace(".json", "")

        for framework in args.frameworks:

            for repeat in range(1, args.repeats + 1):

                completed += 1

                print("\n" + "=" * 70)
                print(
                    f"RUN {completed}/{total_runs} | "
                    f"{task_name} | {framework} | repeat {repeat}"
                )
                print("=" * 70)

                start = time.time()

                command = [
                    sys.executable,
                    os.path.join("runner", "run_task.py"),
                    "--framework",
                    framework,
                    "--task",
                    task_path,
                    "--repeat",
                    str(repeat),
                ]

                try:
                    result = subprocess.run(command, timeout=args.timeout)

                    elapsed = time.time() - start

                    if result.returncode == 0:
                        passed += 1
                        print(
                            f"[BATCH] PASS | "
                            f"{task_name} | {framework} | r{repeat} "
                            f"| {elapsed:.2f}s"
                        )
                    else:
                        failed += 1
                        print(
                            f"[BATCH] FAIL | "
                            f"{task_name} | {framework} | r{repeat} "
                            f"| {elapsed:.2f}s"
                        )

                except subprocess.TimeoutExpired:
                    crashed += 1
                    timed_out += 1
                    elapsed = time.time() - start
                    print(
                        f"[BATCH] TIMEOUT | "
                        f"{task_name} | {framework} | r{repeat} "
                        f"| {elapsed:.2f}s (exceeded {args.timeout}s)"
                    )

                except Exception as e:
                    crashed += 1

                    print(
                        f"[BATCH] CRASH | "
                        f"{task_name} | {framework} | r{repeat}"
                    )
                    print(
                        f"Error: {type(e).__name__}: {e}"
                    )

                # Progress update every 10 runs
                if completed % 10 == 0 or completed == total_runs:
                    elapsed_total = time.time() - overall_start

                    print("\n" + "-" * 70)
                    print("PROGRESS UPDATE")
                    print("-" * 70)
                    print(f"Completed: {completed}/{total_runs}")
                    print(f"Passed:    {passed}")
                    print(f"Failed:    {failed}")
                    print(f"Crashed:   {crashed} (of which {timed_out} timed out)")
                    print(f"Elapsed:   {elapsed_total / 60:.2f} minutes")
                    print("-" * 70)

    total_time = time.time() - overall_start

    print("\n")
    print("=" * 70)
    print("BATCH COMPLETE")
    print("=" * 70)
    print(f"Total runs: {total_runs}")
    print(f"Passed:     {passed}")
    print(f"Failed:     {failed}")
    print(f"Crashed:    {crashed} (of which {timed_out} timed out)")
    print(f"Time:       {total_time / 60:.2f} minutes")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())