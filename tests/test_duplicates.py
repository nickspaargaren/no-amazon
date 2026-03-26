import pytest
from pathlib import Path
from collections import Counter


def test_no_duplicate_domains():
    """Test that amazon.txt contains no duplicate domains."""
    amazon_file = Path(__file__).parent.parent / "amazon.txt"
    
    with open(amazon_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Count occurrences of each domain
    domain_counts = Counter(lines)
    
    # Find duplicates
    duplicates = {domain: count for domain, count in domain_counts.items() if count > 1}
    
    # Assert no duplicates exist
    assert not duplicates, (
        f"Found {len(duplicates)} duplicate domain(s) in amazon.txt:\n" +
        "\n".join(f"  - {domain}: {count} occurrences" for domain, count in duplicates.items())
    )
