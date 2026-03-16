from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys

import torch


def _nvidia_smi_output() -> dict[str, object]:
    try:
        result = subprocess.run(
            ["nvidia-smi", "-L"],
            check=True,
            capture_output=True,
            text=True,
        )
        return {"ok": True, "output": result.stdout.strip()}
    except FileNotFoundError:
        return {"ok": False, "error": "nvidia-smi not found"}
    except subprocess.CalledProcessError as exc:
        return {
            "ok": False,
            "error": exc.stderr.strip() or exc.stdout.strip() or f"exit code {exc.returncode}",
        }


def collect_cuda_report() -> dict[str, object]:
    cuda_available = torch.cuda.is_available()
    report: dict[str, object] = {
        "python_version": sys.version,
        "platform": platform.platform(),
        "torch_version": torch.__version__,
        "torch_version_cuda": torch.version.cuda,
        "cuda_available": cuda_available,
        "device_count": torch.cuda.device_count(),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "nvidia_smi": _nvidia_smi_output(),
    }
    if cuda_available:
        devices = []
        for idx in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(idx)
            devices.append(
                {
                    "index": idx,
                    "name": torch.cuda.get_device_name(idx),
                    "total_memory_gb": props.total_memory / (1024**3),
                    "capability": f"{props.major}.{props.minor}",
                }
            )
        report["devices"] = devices
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Check whether this Python/Torch environment can use CUDA")
    parser.add_argument(
        "--require-cuda",
        action="store_true",
        help="Exit nonzero unless torch.cuda.is_available() is true",
    )
    args = parser.parse_args()

    report = collect_cuda_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.require_cuda and not bool(report["cuda_available"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
