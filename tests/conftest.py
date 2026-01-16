import asyncio
import os
import subprocess
import sys
import time
import pytest
from pathlib import Path

from dotenv import load_dotenv


# Add parent directory to path to import adk_travel_agent module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def pytest_configure(config):
    ensure_test_requirements_installed()
    set_env_vars_on_local_run()


@pytest.fixture(scope="session", autouse=True)
def start_mcp_server():
    """Start the MCP server once per test session."""
    server_process = subprocess.Popen(
        [sys.executable, "weather-mcp-server.py"],
        cwd=Path(__file__).parent.parent,
    )
    time.sleep(2)
    yield
    server_process.terminate()
    server_process.wait()


def set_env_vars_on_local_run():
    """Load environment variables from .env.test for local testing.
    In CI/CD, environment variables should already be set."""
    env_test_path = Path(__file__).parent.parent / '.env.test'
    if env_test_path.exists():
        load_dotenv(env_test_path)


def ensure_test_requirements_installed():
    """Install pytest dependencies before tests run."""
    requirements = Path(__file__).parent / 'requirements.txt'
    if not requirements.exists():
        return

    subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '-r', str(requirements)],
        check=True,
    )