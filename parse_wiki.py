import sys
import xml.etree.ElementTree as etree

fname = sys.argv[1] if len(sys.argv) > 1 else 'wiki20k.xml'

n = 0
nfile = 0
with open(fname) as xml:
    chars_written = 0
    crnt_f = open('{}-{}'.format(fname, nfile), 'w')
    for event, elem in etree.iterparse(xml, events=('end',)):
        if elem.tag.endswith('text'):
            n += 1
            chars_written += crnt_f.write(
                elem.text.lower().replace('\n', ' ') + '\n'
            )
            if chars_written > 4e9:
                print(crnt_f.name)
                crnt_f.close()
                nfile += 1
                chars_written = 0
                crnt_f = open('{}-{}'.format(fname, nfile), 'w')

print(n)
