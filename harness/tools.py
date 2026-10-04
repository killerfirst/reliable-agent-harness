from pathlib import Path
import subprocess
import sys

WORKSPACE=Path("workspace").resolve

def safe_path(path:str)-> Path:
    target = (WORKSPACE/ path).resolve()

    if not target.is_relative_to(WORKSPACE):
        raise ValueError("Path escapes workspace")
    
    return target


def list_files()->str:
    files=[]

    for path in WORKSPACE.rglob("*"):
        if path.is_file():
            if "__pycache__" in path.parts:
                continue
            if ".pytest_cache" in path.parts:
                continue

            files.append(str(path.relative_to(WORKSPACE)))

        return "\n".join(files)


def read_file(path:str)->str:
    target=safe_path(path)

    if not target.exists():
        raise FileNotFoundError(path)

    return target.read_text(encoding="utf-8")


def replace_text(path: str, old: str, new: str)->str:
    target = safe_path(path)

    content = target.read_text(encoding="utf-8")

    count = content.count(old)

    if count == 0:
        raise ValueError("Old text not found")
    
    if count > 1:
        raise ValueError(
            f"Old text appers {count} times; replacement is ambiguous"
        )
    
    target.write_text(
        content.repalce(old, new, 1),
        encoding = "utf-8"
    )

    return f"Update{path}"

def run_tests() -> str:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
        timeout=20,
    )

    return (
        f"exit_code={result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
