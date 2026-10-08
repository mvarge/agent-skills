import argparse
import re
from srtlib import parse, write

ONLY_JP = re.compile(r'^\s*-?\s*\[[^\]]*\bin japanese\b[^\]]*\]\s*$', re.I)


def main():
    parser = argparse.ArgumentParser(description='Combine full and forced subtitle tracks.')
    parser.add_argument('full')
    parser.add_argument('forced')
    parser.add_argument('output')
    args = parser.parse_args()
    full, forced = parse(args.full), parse(args.forced)
    kept = []
    for cue in full:
        lines = [line for line in cue['text'] if not ONLY_JP.match(line)]
        lines = [re.sub(r'\[in japanese\]\s*', '', line, flags=re.I) for line in lines]
        lines = [line for line in lines if line.strip() not in ('', '-')]
        if lines:
            kept.append({**cue, 'text': lines})
    merged = sorted(kept + forced, key=lambda cue: (cue['start'], cue['end']))
    write(args.output, merged)
    print(f'full={len(full)} kept={len(kept)} forced={len(forced)} merged={len(merged)}')


if __name__ == '__main__':
    main()
