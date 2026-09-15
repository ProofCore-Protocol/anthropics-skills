#!/usr/bin/env python3
import sys, json, urllib.request, argparse, os

def main():
    parser = argparse.ArgumentParser(description="ProofCore Fallback Notary")
    parser.add_argument("--file", required=True, help="Path to report file to seal")
    parser.add_argument("--agent", default="agent-skill-fallback", help="Agent ID")
    parser.add_argument("--title", default="Autonomous AI Task", help="Deal Title")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"ERROR|File not found: {args.file}")
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        raw_content = f.read()

    payload = json.dumps({
        "payload": {"mode": "text", "content": raw_content},
        "agent_id": args.agent,
        "title": args.title
    }).encode('utf-8')

    req = urllib.request.Request(
        "https://api.proofcore.org/api/v0.1/seal",
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode('utf-8'))
            print(f"SUCCESS|{res['deal_id']}|{res['sha256_hash']}|{res['citation_markdown']}")
    except Exception as e:
        print(f"ERROR|{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
