import subprocess
from mcp.server.fastmcp import FastMCP
from subfinder import SUBFINDER_BINARY

mcp = FastMCP("no-amazon")


@mcp.tool()
def find_subdomains(domain: str) -> str:
    """Discover subdomains for a given domain using subfinder."""
    result = subprocess.run(
        [str(SUBFINDER_BINARY), "-d", domain, "-silent"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.stdout.strip() or f"No subdomains found for {domain}"


if __name__ == "__main__":
    mcp.run()
