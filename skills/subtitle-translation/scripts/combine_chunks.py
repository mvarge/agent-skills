import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Combine translated chunks in numeric order.')
    parser.add_argument('prefix')
    parser.add_argument('output', type=Path)
    parser.add_argument('--chunks', type=int, default=4)
    args = parser.parse_args()
    paths = [Path(f'{args.prefix}{number}.pt.txt') for number in range(1, args.chunks + 1)]
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        parser.error('missing translated chunks: ' + ', '.join(missing))
    args.output.write_text(''.join(path.read_text(encoding='utf-8') for path in paths), encoding='utf-8')
    print(f'combined {args.chunks} chunks -> {args.output}')


if __name__ == '__main__':
    main()
