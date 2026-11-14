"""Run with python -m predictor. No live-source requests are implemented."""

import argparse
import sys

from .acquisition import register, save_private
from .audit import render
from .records import Invalid, dumps, load_json, validate


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "audit", "register-local"):
        sub = commands.add_parser(name)
        sub.add_argument("registry", help="public candidate registry JSON")
        if name == "audit":
            sub.add_argument("--format", choices=("json", "markdown"), default="markdown")
        if name == "register-local":
            sub.add_argument("--candidate", required=True)
            sub.add_argument("--file", required=True, help="user-supplied local PDF; never copied")
            sub.add_argument("--registered-at", required=True, help="UTC timestamp with Z")
            sub.add_argument("--assessor", required=True, help="non-personal reviewer reference")
            sub.add_argument(
                "--permission-reference",
                required=True,
                help="reviewed private terms/permission reference",
            )
            sub.add_argument(
                "--rights-cleared",
                action="store_true",
                help="affirm human-cleared acquisition AND personal analysis only",
            )
            sub.add_argument(
                "--save",
                help="explicit new receipt path under ignored data/private; otherwise dry-run",
            )
    args = parser.parse_args(argv)
    try:
        registry = validate(load_json(args.registry))
        if args.command == "validate":
            print(
                f"Valid registry {registry['schema_version']}: {len(registry['candidates'])} candidates, {len(registry['slots'])} slots; 0 approved papers."
            )
        elif args.command == "audit":
            sys.stdout.write(render(registry, args.format))
        else:
            ledger = register(
                registry,
                args.candidate,
                args.file,
                registered_at=args.registered_at,
                permission_reference=args.permission_reference,
                assessor=args.assessor,
                rights_cleared=args.rights_cleared,
            )
            if args.save:
                save_private(ledger, args.save)
                print(
                    "Saved private acquisition receipt; public registry unchanged; no approval implied."
                )
            else:
                print("Dry-run PRIVATE receipt; do not commit this output.", file=sys.stderr)
                sys.stdout.write(dumps(ledger))
    except (Invalid, OSError, RecursionError) as exc:
        # OSError messages may contain private paths; never echo them.
        print(
            str(exc) if isinstance(exc, Invalid) else "metadata operation failed", file=sys.stderr
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
