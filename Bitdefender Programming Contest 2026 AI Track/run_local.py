#!/usr/bin/env python3
"""
Evaluation Harness & Benchmark Runner
Bitdefender Programming Contest 2026 - AI Track ("A Tale of Two Suns")

Automates compilation, execution, interactive inter-process piping, logging,
and score aggregation across test blueprint suites.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path


# ---------------------------------------------------------------------------
# Directory & Path Resolution
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent

# Interactor source resolution candidates (in order of preference)
INTERACTOR_CANDIDATES = [
    ROOT_DIR / "judge" / "interactor.cpp",
    ROOT_DIR / "src" / "interactor.cpp",
    ROOT_DIR / "interactor.cpp",
]

# Blueprint directory candidates (in order of preference)
TEST_DIR_CANDIDATES = [
    ROOT_DIR / "data" / "blueprints",
    ROOT_DIR / "public_blueprints",
    ROOT_DIR / "blueprints",
]

# Solution candidates
SOLUTION_CANDIDATES = [
    ROOT_DIR / "src" / "solution.cpp",
    ROOT_DIR / "solution.cpp",
]

BUILD_DIR = ROOT_DIR / "build"
LOGS_DIR = ROOT_DIR / "logs"
BIN_PREFIX = "bpc_2026_"


def get_interactor_src() -> Path:
    for candidate in INTERACTOR_CANDIDATES:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"Judge interactor source not found. Searched in: {[str(p) for p in INTERACTOR_CANDIDATES]}"
    )


def get_default_test_dir() -> Path:
    for candidate in TEST_DIR_CANDIDATES:
        if candidate.is_dir():
            return candidate
    return ROOT_DIR / "data" / "blueprints"


def get_default_solution() -> Path:
    for candidate in SOLUTION_CANDIDATES:
        if candidate.is_file():
            return candidate
    return ROOT_DIR / "src" / "solution.cpp"


def bin_path(name: str) -> Path:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    suffix = ".exe" if sys.platform == "win32" else ""
    return BUILD_DIR / f"{name}{suffix}"


def find_test_files(test_dir: Path) -> list[Path]:
    files = list(test_dir.glob("*.in")) + list(test_dir.glob("*.txt"))
    return sorted(files, key=lambda p: p.name)


def needs_recompile(source: Path, binary: Path) -> bool:
    if not binary.exists():
        return True
    return binary.stat().st_mtime < source.stat().st_mtime


def require_tool(*candidates: str, env_var: str | None = None) -> str:
    if env_var:
        val = os.environ.get(env_var)
        if val and shutil.which(val):
            return val
    for cmd in candidates:
        if shutil.which(cmd):
            return cmd
    print(
        f"Error: none of {list(candidates)} found on system PATH. Please ensure a compatible compiler is installed.",
        file=sys.stderr,
    )
    sys.exit(1)


def compile_interactor() -> Path:
    src = get_interactor_src()
    out = bin_path(f"{BIN_PREFIX}interactor")
    if needs_recompile(src, out):
        print(f"[BUILD] Compiling evaluation judge ({src.name})...", flush=True)
        cxx = require_tool("g++", "clang++", "c++", env_var="CXX")
        subprocess.run(
            [cxx, "-std=c++17", "-O2", "-o", str(out), str(src)],
            check=True,
        )
    return out


def resolve_solution_path(sol_arg: str) -> Path:
    p = Path(sol_arg)
    if p.is_file():
        return p.resolve()
    # Try resolving relative to root or src
    for base in [ROOT_DIR, ROOT_DIR / "src", ROOT_DIR / "src" / "baselines"]:
        cand = (base / sol_arg).resolve()
        if cand.is_file():
            return cand
    return p.resolve()


def java_main_class(sol_src: Path) -> str:
    with open(sol_src, encoding="utf-8") as f:
        source = f.read()

    package = re.search(r"^\s*package\s+([\w.]+)\s*;", source, re.MULTILINE)
    public_class = re.search(r"\bpublic\s+class\s+(\w+)\b", source)
    main_class = re.search(
        r"\bclass\s+(\w+)\b[\s\S]*?\bpublic\s+static\s+void\s+main\s*\(",
        source,
    )

    if public_class:
        class_name = public_class.group(1)
    elif main_class:
        class_name = main_class.group(1)
    else:
        class_name = sol_src.stem

    if package:
        return f"{package.group(1)}.{class_name}"
    return class_name


def solution_command(sol_src: Path) -> list[str]:
    ext = sol_src.suffix.lower()
    name = sol_src.stem

    if ext in (".cpp", ".cc", ".cxx"):
        out = bin_path(f"{BIN_PREFIX}{name}")
        if needs_recompile(sol_src, out):
            print(f"[BUILD] Compiling C++ solution ({sol_src.name})...", flush=True)
            cxx = require_tool("g++", "clang++", "c++", env_var="CXX")
            subprocess.run(
                [cxx, "-std=c++17", "-O2", "-o", str(out), str(sol_src)],
                check=True,
            )
        return [str(out)]

    if ext == ".c":
        out = bin_path(f"{BIN_PREFIX}{name}")
        if needs_recompile(sol_src, out):
            print(f"[BUILD] Compiling C solution ({sol_src.name})...", flush=True)
            cc = require_tool("gcc", "clang", "cc", env_var="CC")
            subprocess.run(
                [cc, "-std=c11", "-O2", "-o", str(out), str(sol_src)],
                check=True,
            )
        return [str(out)]

    if ext == ".py":
        return [sys.executable, "-u", str(sol_src)]

    if ext == ".rs":
        out = bin_path(f"{BIN_PREFIX}{name}")
        if needs_recompile(sol_src, out):
            print(f"[BUILD] Compiling Rust solution ({sol_src.name})...", flush=True)
            rustc = require_tool("rustc")
            subprocess.run([rustc, "-O", "-o", str(out), str(sol_src)], check=True)
        return [str(out)]

    if ext == ".java":
        bin_dir = BUILD_DIR / f"{BIN_PREFIX}{name}_classes"
        if needs_recompile(sol_src, bin_dir):
            bin_dir.mkdir(parents=True, exist_ok=True)
            print(f"[BUILD] Compiling Java solution ({sol_src.name})...", flush=True)
            javac = require_tool("javac")
            subprocess.run([javac, "-d", str(bin_dir), str(sol_src)], check=True)
        java = require_tool("java")
        return [java, "-cp", str(bin_dir), java_main_class(sol_src)]

    supported = ".c, .cpp/.cc/.cxx, .py, .java, .rs"
    print(f"Error: Unsupported file extension '{ext}' (supported: {supported})", file=sys.stderr)
    sys.exit(1)


def forward(src, dst, name: str, log=None, scores: list[int] | None = None):
    try:
        for line in iter(src.readline, ""):
            if not line:
                break
            if log:
                log.write(f"[{name}] {line}")
                log.flush()
            if "SCORE:" in line and scores is not None:
                match = re.search(r"SCORE:\s*(\d+)", line)
                if match:
                    scores.append(int(match.group(1)))

            dst.write(line)
            dst.flush()
    except (BrokenPipeError, OSError):
        pass

    try:
        dst.close()
    except Exception:
        pass


def run_single_test(
    interactor_bin: Path,
    sol_cmd: list[str],
    test_file: Path,
    log_path: Path | None = None,
) -> int | None:
    log = None
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log = open(log_path, "w", encoding="utf-8")

    # Spawn participant solution
    sol = subprocess.Popen(
        sol_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    # Spawn contest interactor/judge
    inter = subprocess.Popen(
        [str(interactor_bin), str(test_file)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1,
        **({"creationflags": 0} if sys.platform == "win32" else {}),
    )

    scores: list[int] = []

    t1 = threading.Thread(
        target=forward,
        args=(inter.stdout, sol.stdin, "INTERACTOR → SOLUTION", log, scores),
    )
    t2 = threading.Thread(
        target=forward,
        args=(sol.stdout, inter.stdin, "SOLUTION → INTERACTOR", log, None),
    )

    t1.start()
    t2.start()

    inter.wait()
    sol.wait()

    t1.join()
    t2.join()

    if log:
        log.close()

    failed = False
    if inter.returncode != 0:
        print(f"Interactor exited with code {inter.returncode}", file=sys.stderr)
        failed = True
    if sol.returncode != 0:
        print(f"Solution exited with code {sol.returncode}", file=sys.stderr)
        failed = True

    if failed:
        return None

    return scores[0] if scores else 0


def cleanup_generated_files():
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
        print(f"Removed build directory: {BUILD_DIR}")
    if LOGS_DIR.exists():
        for f in LOGS_DIR.glob("*.log"):
            try:
                f.unlink()
            except OSError:
                pass
        print(f"Cleaned log files in: {LOGS_DIR}")
    # Also clean legacy bin prefixes if any remain in root
    for path in ROOT_DIR.glob(f"{BIN_PREFIX}*"):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        else:
            try:
                path.unlink()
            except OSError:
                pass


def main():
    if "--" in sys.argv:
        sep = sys.argv.index("--")
        script_args = sys.argv[1:sep]
        sol_cmd = sys.argv[sep + 1 :]
        if not sol_cmd:
            print("Error: expected a command after '--'", file=sys.stderr)
            sys.exit(1)
    else:
        script_args = sys.argv[1:]
        sol_cmd = None

    default_sol = str(get_default_solution())
    default_test_dir = str(get_default_test_dir())

    parser = argparse.ArgumentParser(
        description="BPC 2026 AI Track Benchmark & Evaluation Harness"
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["clean"],
        help="Remove compiled binaries and execution log traces",
    )
    parser.add_argument(
        "--test-dir",
        default=default_test_dir,
        help=f"Path to directory containing blueprint files (.in) (default: {default_test_dir})",
    )
    parser.add_argument(
        "-t",
        "--test",
        default=None,
        help="Run a single test blueprint file instead of the full suite.",
    )
    parser.add_argument(
        "-s",
        "--solution",
        default=default_sol,
        help=f"Path to solution source file (.cpp, .c, .py, .rs, .java) (default: {default_sol})",
    )
    args = parser.parse_args(script_args)

    if args.command == "clean":
        cleanup_generated_files()
        print("Cleanup completed successfully.")
        return

    try:
        interactor_bin = compile_interactor()

        if sol_cmd:
            sol_stem = "custom_command"
            print(f"[RUN] Using custom solution command: {' '.join(sol_cmd)}\n", flush=True)
        else:
            sol_path = resolve_solution_path(args.solution)
            if not sol_path.is_file():
                print(f"Error: Solution file not found: {args.solution}", file=sys.stderr)
                sys.exit(1)
            sol_stem = sol_path.stem
            sol_cmd = solution_command(sol_path)

        if args.test:
            tp = Path(args.test)
            if not tp.is_file():
                # Check inside default test directory
                cand = Path(args.test_dir) / args.test
                if cand.is_file():
                    tp = cand
                else:
                    print(f"Error: Test file not found: {args.test}", file=sys.stderr)
                    sys.exit(1)
            test_files = [tp.resolve()]
        else:
            td = Path(args.test_dir)
            if not td.is_dir():
                print(f"Error: Test directory not found: {td}", file=sys.stderr)
                sys.exit(1)
            test_files = find_test_files(td)
            if not test_files:
                print(f"Error: No test blueprint files (.in) found in: {td}", file=sys.stderr)
                sys.exit(1)

        print(f"\n{'=' * 65}")
        print(f" Bitdefender Programming Contest 2026 - Evaluation Suite")
        print(f"{'=' * 65}")
        print(f" Solution:   {args.solution}")
        print(f" Blueprints: {len(test_files)} test suite(s)")
        print(f" Logs:       {LOGS_DIR}")
        print(f"{'=' * 65}\n")

        total_score = 0
        any_failed = False
        results: list[tuple[str, int | str]] = []

        for tf in test_files:
            test_stem = tf.stem
            log_path = LOGS_DIR / f"{sol_stem}__{test_stem}.log"
            score = run_single_test(interactor_bin, sol_cmd, tf, log_path=log_path)

            if score is None:
                results.append((tf.name, "FAILED"))
                print(f"[-] {tf.name:<25} FAILED (check {log_path.name})")
                any_failed = True
            else:
                results.append((tf.name, score))
                total_score += score
                print(f"[+] {tf.name:<25} SCORE: {score:>6}")

        print(f"\n{'-' * 65}")
        print(f" TOTAL EVALUATION SCORE: {total_score:>37}")
        print(f"{'-' * 65}\n")

        if any_failed:
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"Execution/Compilation error (exit code {e.returncode})", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

