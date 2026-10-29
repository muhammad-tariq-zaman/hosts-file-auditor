"""Audit a hosts file: flag invalid IPs and duplicate hostnames.

Usage: python3 main.py hosts.txt
"""
import argparse
import ipaddress
import sys


def parse_hosts(text):
    """Return a list of (ip, [hostnames]) entries, skipping comments/blanks."""
    entries = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            entries.append((parts[0], parts[1:]))
    return entries


def audit(entries):
    """Return a list of human-readable issue strings."""
    issues = []
    seen_host = {}
    for ip, hosts in entries:
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            issues.append(f"Invalid IP address: {ip}")
        for host in hosts:
            # Same hostname on IPv4 and IPv6 (e.g. localhost) is normal.
            try:
                same_family = (ipaddress.ip_address(ip).version ==
                               ipaddress.ip_address(seen_host[host]).version)
            except (ValueError, KeyError):
                same_family = True
            if host in seen_host and seen_host[host] != ip and same_family:
                issues.append(
                    f"Duplicate hostname {host}: mapped to both "
                    f"{seen_host[host]} and {ip}"
                )
            else:
                seen_host[host] = ip
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to a hosts-style file")
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        entries = parse_hosts(f.read())
    issues = audit(entries)
    print(f"Checked {len(entries)} entries, {len(issues)} issue(s).")
    for issue in issues:
        print(f"- {issue}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
