#!/usr/bin/env python3
"""Render a dashboard from a local entity map. Never writes to Home Assistant or GitHub."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r'__([A-Z][A-Z0-9_]+)__')
ENTITY = re.compile(r'^[a-z][a-z0-9_]*\.[a-z0-9_]+$')
DOMAINS = {
    'POWER_ENTITY':'select', 'OPERATION_ENTITY':'sensor', 'CONNECTED_ENTITY':'binary_sensor',
    'REMOTE_ENTITY':'binary_sensor', 'CHILD_LOCK_ENTITY':'binary_sensor',
    'TEMPERATURE_ENTITY':'select', 'BEANS_ENTITY':'select', 'QUANTITY_ENTITY':'number',
    'MULTIPLE_ENTITY':'switch', 'MILK_COUNTER_ENTITY':'sensor', 'COFFEE_COUNTER_ENTITY':'sensor',
    'ESPRESSO_COUNTER_ENTITY':'sensor', 'WATER_COUNTER_ENTITY':'sensor',
    'COFFEE_SCRIPT':'script', 'ESPRESSO_SCRIPT':'script', 'CAPPUCCINO_SCRIPT':'script',
    'LATTE_SCRIPT':'script', 'TEA_SCRIPT':'script',
}

def render(template: str, mapping: dict[str, str]) -> str:
    if not isinstance(mapping, dict):
        raise ValueError('Die Zuordnung muss ein JSON-Objekt sein.')
    unknown = set(mapping) - set(DOMAINS)
    if unknown:
        raise ValueError('Unbekannte Schlüssel: ' + ', '.join(sorted(unknown)))
    required = set(TOKEN.findall(template))
    missing = required - set(mapping)
    if missing:
        raise ValueError('Diese Zuordnungen fehlen: ' + ', '.join(sorted(missing)))
    for key in required:
        value = mapping[key]
        if not isinstance(value,str) or not ENTITY.fullmatch(value):
            raise ValueError(f'{key}: eine gültige Entity-ID wie script.mein_kaffee eintragen.')
        if value.split('.')[0] != DOMAINS[key]:
            raise ValueError(f'{key}: erwartet wird die Domain {DOMAINS[key]}.')
    return TOKEN.sub(lambda m: mapping[m.group(1)], template)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--style', choices=['native','barista'], default='native')
    parser.add_argument('--mapping', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    name = 'quick_start.template.yaml' if args.style == 'native' else 'barista.template.yaml'
    try:
        mapping = json.loads(args.mapping.read_text(encoding='utf-8'))
        result = render((ROOT/'dashboards'/name).read_text(encoding='utf-8'), mapping)
        # Exclusive creation: no accidental overwrite of a user's edited dashboard.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as handle:
            handle.write(result)
    except (OSError, ValueError) as exc:
        print(f'Nicht erstellt: {exc}', file=sys.stderr)
        return 1
    print(f'Erstellt: {args.output}. Lokal prüfen und erst danach in ein NEUES Dashboard übernehmen.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
