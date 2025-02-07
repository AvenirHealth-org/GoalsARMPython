# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "docopt",
# ]
# ///
"""
Should be run inside a venv, run it via uv e.g. "uv run compile --local"
Usage:
  compile.py [--local] [--debug] [--force]
  compile.py (-h | --help)

Options:
  --local     Enable local build mode.
  --debug     Enable debug build mode.
  --force     Force running even outside of a virtual environment.
  -h --help   Show this help message.
"""

import os
import subprocess
import sys
from docopt import docopt

def is_virtual_env():
    """Checks if the script is running inside a virtual environment."""
    return sys.prefix != sys.base_prefix

def run_build(local, debug, force):
    """Run the build with appropriate environment variables."""
    if not is_virtual_env() and not force:
        print("This script should be run via uv `uv run ./scripts/compile.py`. Use --force to override.")
        sys.exit(1)

    env = os.environ.copy()

    if local:
        env["LOCAL_BUILD"] = "true"
        print("Compiling against local sources...")

    if debug:
        env["DEBUG_BUILD"] = "true"
        print("Compiling with debug symbols...")
    else:
        print("Compiling in release mode...")

    # Replace this with your actual build command
    subprocess.check_call([
        "uv", "sync", "-v", "--reinstall-package", "goals"
    ], env=env)

if __name__ == "__main__":
    # Parse the command-line arguments using docopt
    arguments = docopt(__doc__)

    # Extract the options
    local = arguments['--local']
    debug = arguments['--debug']
    force = arguments['--force']

    # Run the build process
    run_build(local=local, debug=debug, force=force)
