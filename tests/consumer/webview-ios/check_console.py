"""Verify the independent Swift app's bounded WKWebView transport on the owned simulator."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import time


APP = "io.github.apdelrahman1911.nativecmpkit.consumer.wkwebview"
PASS = "NATIVECMPKIT_PACKAGED_WKWEBVIEW_PASS"
FAIL = "NATIVECMPKIT_PACKAGED_WKWEBVIEW_FAIL"


def verify(simulator, output):
    log = output / "console.log"
    command = ["xcrun", "simctl", "launch", "--console", simulator, APP]
    with log.open("xb") as capture, subprocess.Popen(command, stdout=capture, stderr=subprocess.STDOUT) as run:
        try:
            started = time.monotonic()
            while time.monotonic() - started < 65:
                if log.stat().st_size > 256 * 1024:
                    raise ValueError("WKWebView consumer console exceeded its bound")
                lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
                if any(line.startswith(FAIL) for line in lines) or lines.count(PASS) > 1:
                    raise ValueError("The published WKWebView consumer reported a failure")
                if lines.count(PASS) == 1 and run.poll() is None:
                    result = {"revision": os.environ["GITHUB_SHA"], "simulator": simulator, "argv": command,
                              "completed_cases": 1, "passed_cases": 1, "elapsed_seconds": time.monotonic() - started}
                    with (output / "result.json").open("x", encoding="utf-8") as report:
                        json.dump(result, report, indent=2)
                        report.write("\n")
                    return
                if run.poll() is not None:
                    raise ValueError(f"The independent consumer exited before acceptance: {run.returncode}")
                time.sleep(0.25)
            raise TimeoutError("Timed out loading or disposing the packaged WKWebView")
        finally:
            if run.poll() is None:
                run.kill()
                run.wait(timeout=10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("simulator")
    parser.add_argument("output", type=Path)
    options = parser.parse_args()
    verify(options.simulator, options.output)
