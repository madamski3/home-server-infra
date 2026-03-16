import subprocess


def run_compose_service(compose_file: str, service: str, args: list[str]) -> dict:
    """Run a one-off docker compose service and return the result."""
    cmd = ["docker", "compose", "-f", compose_file, "run", "--rm", service] + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return {
        "success": result.returncode == 0,
        "returncode": result.returncode,
        "output": result.stdout + result.stderr,
    }
