import argparse
import re
from pathlib import Path


def markers(path):
    seen = []
    current = None
    for line in path.read_text(encoding='utf-8').replace('\r', '').split('\n'):
        match = re.fullmatch(r'###\s*(\d+)\s*', line)
        if match:
            current = int(match.group(1))
            seen.append((current, 0))
        elif current is not None and line.strip():
            cue, count = seen[-1]
            seen[-1] = (cue, count + 1)
    return seen


def main():
    parser = argparse.ArgumentParser(description='Validate translated chunk coverage.')
    parser.add_argument('directory', type=Path)
    parser.add_argument('--chunks', type=int, default=4)
    args = parser.parse_args()
    failures = []
    for number in range(1, args.chunks + 1):
        english = args.directory / f'chunk{number}.en.txt'
        translated = args.directory / f'chunk{number}.pt.txt'
        expected = [cue for cue, _ in markers(english)]
        actual = markers(translated) if translated.exists() else []
        if not expected or [cue for cue, _ in actual] != expected or any(count < 1 for _, count in actual):
            failures.append(f'chunk{number}: expected {expected[0]}-{expected[-1]} with one translation per cue')
        else:
            print(f'OK {expected[0]}-{expected[-1]}')
    if failures:
        print('\n'.join(failures))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
