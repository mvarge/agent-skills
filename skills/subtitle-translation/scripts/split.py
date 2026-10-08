import argparse
from pathlib import Path
from srtlib import parse


def main():
    parser = argparse.ArgumentParser(description='Split an SRT into cue-numbered text chunks.')
    parser.add_argument('source')
    parser.add_argument('prefix', help='Output prefix, such as work/chunk')
    parser.add_argument('--chunks', type=int, default=4)
    args = parser.parse_args()
    cues = parse(args.source)
    if args.chunks < 1 or args.chunks > len(cues):
        parser.error('--chunks must be between 1 and the cue count')
    bounds = [round(i * len(cues) / args.chunks) for i in range(args.chunks + 1)]
    for number, (start, end) in enumerate(zip(bounds, bounds[1:]), 1):
        output = Path(f'{args.prefix}{number}.en.txt')
        with output.open('w', encoding='utf-8') as handle:
            for index in range(start, end):
                handle.write(f"### {index + 1}\n")
                handle.write('\n'.join(cues[index]['text']) + '\n')
        print(f'chunk{number}: cues {start + 1}-{end} -> {output}')


if __name__ == '__main__':
    main()
