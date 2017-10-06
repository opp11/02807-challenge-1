import sys
import xml.etree.ElementTree as etree

def parse_wiki(xmlfile, outfile=None):
    if outfile is None:
        outfile = xmlfile + '-all'
    with open(xmlfile) as xml, open(outfile, 'w') as out:
        for event, elem in etree.iterparse(xml, events=('end',)):
            if elem.tag.endswith('text') and elem.text is not None and not \
                elem.text.lower().startswith('#redirect'):
                out.write(
                    elem.text.lower().replace('\n', ' ') + '\n'
                )
            elem.clear()


def main(argv):
    if len(argv) < 2:
        raise ValueError('Must supply xml file name')

    xmlfile = argv[1]
    outfile = argv[2] if len(argv) > 2 else None
    parse_wiki(xmlfile, outfile)


if __name__ == '__main__':
    main(sys.argv)
