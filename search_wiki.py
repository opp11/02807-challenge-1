import subprocess
import re
import sys

def make_grep_pattern(pattern):
    pattern = pattern.strip()
    parts = re.split(r'(".+?")', pattern)

    if len(parts[0]) > 0:
        raise ValueError('Pattern must start with a string')

    grep_pattern = ""
    for part in parts[1:]:
        part = part.strip()
        if len(part) == 0:
            continue
        elif part.startswith('"') and part.endswith('"'):
            grep_pattern += part[1:-1]
        elif part.startswith('[') and part.endswith(']'):
            nums = re.match(r'\[\s*(\d+?)\s*,\s*(\d+?)\s*\]', part)
            if nums is None:
                raise ValueError('Wildcards must have the form [A,B], where A and B are numbers')
            nums = list(map(int, nums.groups()))
            grep_pattern += '.{' + str(nums[0]) + ',' + str(nums[1]) + '}'
        else:
            raise ValueError('Invalid pattern')

    return grep_pattern


def make_grep_cmd(pattern, filename):
    cmd = ['rg']
    cmd.append(make_grep_pattern(pattern))
    cmd.append(filename)
    cmd.append('-o')
    cmd.append('-N')

    return cmd


def search_wiki(pattern, wikifile):
    cmd = make_grep_cmd(pattern, wikifile)
    res = subprocess.check_output(cmd)
    return res.decode('utf-8').split('\n')


def main(argv):
    if len(argv) < 2:
        raise ValueError('Must supply two command line arguments')

    pattern = argv[1]
    wikifile = argv[2]
    for r in search_wiki(pattern, wikifile):
        print(r)


if __name__ == '__main__':
    main(sys.argv)
