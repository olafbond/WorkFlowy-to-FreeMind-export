import os
import glob

working_dir = 'C:/Users/o1af/Desktop/'


def clean_line(line):
    line = line.strip()
    line = line.replace('&lt;', '')
    line = line.replace('/b&gt;', '')
    line = line.replace('b&gt;', '')
    return line


def get_attr(line, substring):
    text_start = line.find(substring) + len(substring)  # getting text attribute
    text_end = line.find('"', text_start)
    substring = line[text_start:text_end]
    return substring.strip()


working_dir = os.path.expanduser(working_dir)  # adapting path string to OS
wf_files = glob.glob(working_dir+'WF*.opml')

for wf_file in wf_files:
    with open(wf_file, "rt", encoding='utf_8') as wf:
        xml = ''                    # output xml in FreeMind format
        id = 0                      # node's ID
        level = 0                   # node's level
        left_nodes = 0              # number of nodes to the left
        right_nodes = 0             # number of nodes to the right

        for line in wf:
            line = clean_line(line)                     # cleaning from spaces, tags, etc.
            if line[:6] == '<body>':                    # here is the data
                xml = xml + '<map version="1.0.1">\n'   # xml header
            elif line[:7] == '</body>':                 # data ends
                xml = xml + '</map>\n'                  # and our xml
            elif line[:8] == '<outline':                # a node here
                id = id + 1
                xml = xml + f'<node ID="{id}" '

                text = get_attr(line, 'text="')
                xml = xml + f'TEXT="{text}" '

                if level == 1:                          # children are placed in some order
                    note = get_attr(line, '_note="')
                    if note[:5] == 'right':
                        xml = xml + f'POSITION="right" '
                        right_nodes = right_nodes + 1
                    elif note[:4] == 'left':
                        xml = xml + f'POSITION="left" '
                        left_nodes = left_nodes + 1
                    elif left_nodes < right_nodes:
                        xml = xml + f'POSITION="left" '
                        left_nodes = left_nodes + 1
                    else:
                        xml = xml + f'POSITION="right" '
                        right_nodes = right_nodes + 1

                if line[-2:] == '/>':                   # closing of a tag inline
                    xml = xml + '/>\n'                  # we do the same
                else:                                   # not colosed tag
                    xml = xml + '>\n'                   # we do the same
                    level = level + 1                   # incresed level of the next node

            elif line[:10] == '</outline>':             # closing of a tag in a separate line
                xml = xml + '</node>\n'                 # we do the same
                level = level - 1                       # decresed level of the next node
            else:
                pass

    fm_file = wf_file + ".mm"                           # writing FreeMind .mm file
    with open(fm_file, 'w', encoding='utf_8') as fm:
        fm.write(xml)
