"""CLI do motor de reembolso."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="reembolso")
    sub = parser.add_subparsers(dest="command")

    calc = sub.add_parser("calcular", help="Calcula reembolso a partir de JSON de despesas")
    calc.add_argument("--input", required=True, help="Caminho do JSON de entrada")
    calc.add_argument("--output", required=True, help="Caminho do JSON de saída")
    calc.add_argument(
        "--politica",
        required=True,
        help="Caminho do JSON de política (ex.: politica-v4.json)",
    )
    calc.add_argument(
        "--cambio",
        required=True,
        help="Caminho do JSON de câmbio (ex.: cambio.json)",
    )

    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "calcular":
        from reembolso.cli.calcular_cmd import run_calcular  # noqa: PLC0415

        return run_calcular(args.input, args.output, args.politica, args.cambio)
    return 1


if __name__ == "__main__":
    sys.exit(main())
