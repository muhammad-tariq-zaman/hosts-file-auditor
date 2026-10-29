# hosts-file-auditor

Audit a hosts file: flags invalid IP addresses and hostnames that are
mapped to two different IPs. Comments and blank lines are ignored.

## How to run

```bash
python3 main.py hosts.txt
```

## Example output

```text
Checked 3 entries, 1 issue(s).
- Duplicate hostname web: mapped to both 10.0.0.1 and 10.0.0.2
```

Standard library only. No network access.
