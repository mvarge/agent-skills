import re

TS = re.compile(r'(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)')


def ms(h, m, s, f):
    return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(f)


def fmt(t):
    h, t = divmod(t, 3600000)
    m, t = divmod(t, 60000)
    s, f = divmod(t, 1000)
    return f"{h:02}:{m:02}:{s:02},{f:03}"


def parse(path):
    cues = []
    blocks = re.split(r'\n\s*\n', open(path, encoding='utf-8-sig').read().replace('\r', ''))
    for block in blocks:
        lines = block.strip().split('\n')
        for index, line in enumerate(lines):
            match = TS.search(line)
            if match:
                group = match.groups()
                cues.append({'start': ms(*group[:4]), 'end': ms(*group[4:]),
                             'text': [x for x in lines[index + 1:] if x.strip()]})
                break
    return cues


def write(path, cues):
    with open(path, 'w', encoding='utf-8') as output:
        for index, cue in enumerate(cues, 1):
            output.write(f"{index}\n{fmt(cue['start'])} --> {fmt(cue['end'])}\n")
            output.write('\n'.join(cue['text']) + '\n\n')
