#!/usr/bin/env python3
"""Generate unique CloudFront redirect HTML files."""
import hashlib
import os
import sys
import time

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="0;url={target}">
<title>Redirecting...</title>
</head>
<body>
<p>Redirecting... <a href="{target}">Click here</a></p>
</body>
</html>"""

def generate_id() -> str:
    raw = f"{time.time_ns()}{os.urandom(8).hex()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:8]

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "redirects")
    os.makedirs(out_dir, exist_ok=True)

    generated = []
    for _ in range(count):
        uid = generate_id()
        filepath = os.path.join(out_dir, f"{uid}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(TEMPLATE.format(target=target))
        generated.append(uid)

    base = "https://dmdgnvthvqht6.cloudfront.net/r"
    print(f"Generated {count} redirects -> {target}")
    for uid in generated:
        print(f"  {base}/{uid}.html")

if __name__ == "__main__":
    main()
