import platform, stat, urllib.request, zipfile
from pathlib import Path

if platform.system() != "Darwin" or platform.machine() != "arm64":
    raise RuntimeError("Only macOS Apple Silicon is supported")

SUBFINDER_BINARY = Path(__file__).parent / "bin" / "subfinder"

if not SUBFINDER_BINARY.exists():
    SUBFINDER_BINARY.parent.mkdir(parents=True, exist_ok=True)
    zip_path = SUBFINDER_BINARY.with_suffix(".zip")
    urllib.request.urlretrieve(
        "https://github.com/projectdiscovery/subfinder/releases/download/v2.14.0/subfinder_2.14.0_macOS_arm64.zip",
        zip_path,
    )
    with zipfile.ZipFile(zip_path) as z:
        z.extract("subfinder", SUBFINDER_BINARY.parent)
    zip_path.unlink()
    SUBFINDER_BINARY.chmod(SUBFINDER_BINARY.stat().st_mode | stat.S_IEXEC)
