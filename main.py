import os
import glob

WORKING_DIR = 'C:/Users/o1af/Desktop/'
MOVE_COMPLETED_LEFT = True
MINDMAP_AUTOSTART = True
MINDMAP_COMMAND = 'C:/Program Files (x86)/FreeMind/FreeMind.exe'


def clean_line(line):
    line = line.strip()
    line = line.replace('&lt;', '')
    line = line.replace('/b&gt;', '')
    line = line.replace('b&gt;', '')
    return line


def get_attr(line, substring):
    substring = substring + '="'
    text_start = line.find(substring) + len(substring)  # getting text attribute
    text_end = line.find('"', text_start)
    if text_start > 0 and text_end > text_start:
        substring = line[text_start:text_end].strip()
    else:
        substring = ""
    return substring


def read_wf_file(wf_file):
    with open(wf_file, "rt", encoding='utf_8') as wf:
        xml = ''                    # output xml in FreeMind format
        id = 0                      # node's ID
        level = 0                   # node's level
        left_nodes = 0              # number of nodes to the left
        right_nodes = 0             # number of nodes to the right

        for line in wf:
            line = clean_line(line)

            if line[:6] == '<body>':                    # here is the data
                xml = xml + '<map version="1.0.1">\n'   # xml header
            elif line[:7] == '</body>':                 # data ends
                xml = xml + '</map>\n'                  # and our xml

            elif line[:8] == '<outline':                # a node here
                id = id + 1
                xml = xml + f'<node ID="{id}" '

                complete = get_attr(line, '_complete')
                if complete == 'true':
                    xml = xml + f'BACKGROUND_COLOR="#cccccc" '


                text = get_attr(line, 'text')
                if text != '':
                    xml = xml + f'TEXT="{text}" '

                # children of level 1 are placed in some order
                if level == 1:
                    note = get_attr(line, '_note')

                    if note[:5] == 'right':
                        xml = xml + f'POSITION="right" '
                        right_nodes = right_nodes + 1
                    elif note[:4] == 'left' \
                            or (complete == 'true' and MOVE_COMPLETED_LEFT) \
                            or left_nodes < right_nodes:
                        xml = xml + f'POSITION="left" '
                        left_nodes = left_nodes + 1
                    else:
                        xml = xml + f'POSITION="right" '
                        right_nodes = right_nodes + 1

                # closing of a tag inline
                if line[-2:] == '/>':
                    xml = xml + '/>\n'                  # we do the same
                else:                                   # not colosed tag
                    xml = xml + '>\n'                   # we do the same
                    level = level + 1                   # incresed level of the next node

            # closing of a tag in a separate line
            elif line[:10] == '</outline>':
                xml = xml + '</node>\n'                 # we do the same
                level = level - 1                       # decresed level of the next node

            else:
                pass


    return xml


def main():
    working_dir = os.path.expanduser(WORKING_DIR)  # adapting path string to OS
    wf_files = glob.glob(working_dir+'WF*.opml')

    for wf_file in wf_files:
        xml = read_wf_file(wf_file)

        fm_file = wf_file + ".mm"                            # writing FreeMind .mm file
        fm_file = fm_file.replace(' ','-')
        with open(fm_file, 'w', encoding='utf_8') as fm:
            fm.write(xml)

        if MINDMAP_AUTOSTART:
            cmdline = '"' + os.path.expanduser(MINDMAP_COMMAND) + '" ' + fm_file
            os.system(cmdline)


if __name__ == "__main__":
    main()
