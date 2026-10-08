import argparse
import re
from srtlib import parse, write


def main():
    parser = argparse.ArgumentParser(description='Put translated text onto source SRT timestamps.')
    parser.add_argument('source')
    parser.add_argument('translation')
    parser.add_argument('output')
    args = parser.parse_args()
    cues = parse(args.source)
    translated = {}
    current = None
    for line in open(args.translation, encoding='utf-8').read().replace('\r', '').split('\n'):
        match = re.fullmatch(r'###\s*(\d+)\s*', line)
        if match:
            current = int(match.group(1))
            if current in translated:
                raise SystemExit(f'DUPLICATE {current}')
            translated[current] = []
        elif current is not None and line.strip():
            translated[current].append(line.rstrip())
    missing = [index for index in range(1, len(cues) + 1) if not translated.get(index)]
    extra = [index for index in translated if index < 1 or index > len(cues)]
    if missing or extra:
        print(f'MISSING {missing[:20]} EXTRA {extra[:20]}')
        raise SystemExit(1)
    write(args.output, [{**cue, 'text': translated[index]} for index, cue in enumerate(cues, 1)])
    print(f'OK cues: {len(cues)}')


if __name__ == '__main__':
    main()
