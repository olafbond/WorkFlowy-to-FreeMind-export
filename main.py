import os
import glob
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


WORKING_DIR = 'C:/Users/o1af/Desktop/'
WATCHDOG = True
MOVE_COMPLETED_LEFT = True
MINDMAP_AUTOSTART = True
MINDMAP_COMMAND = 'C:/Program Files (x86)/FreeMind/FreeMind.exe'


def rem_attr(line):
    # cleaning a line of text from leading spaces and secorating elements
    line = line.strip()
    attr_found = True
    while attr_found:
        attr_start = line.find('&lt;')
        attr_end = line.find('&gt;', attr_start) + len('&gt;')
        if attr_start > 0 and attr_end > attr_start:
            line = line.replace(line[attr_start:attr_end],'')
        else:
            attr_found = False
    return line


def get_attr(line, substring):
    # searching for a given atribute
    substring = substring + '="'
    attr_start = line.find(substring) + len(substring)
    attr_end = line.find('"', attr_start)
    if attr_start > 0 and attr_end > attr_start:
        substring = line[attr_start:attr_end].strip()
    else:
        substring = ""
    return substring


def read_wf_file(wf_file):
    # reading opml file and translating into xml of mm file
    with open(wf_file, "rt", encoding='utf_8') as wf:
        xml = ''                    # output xml in FreeMind format
        id = 0                      # node's ID
        level = 0                   # node's level
        left_nodes = 0              # number of nodes to the left
        right_nodes = 0             # number of nodes to the right

        for line in wf:
            line = rem_attr(line)

            if line[:6] == '<body>':                    # here is the data
                xml = xml + '<map version="1.0.1">\n'   # xml header
            elif line[:7] == '</body>':                 # data ends
                xml = xml + '</map>\n'                  # and our xml

            elif line[:8] == '<outline':                # a node is here
                # assining node's ID
                id = id + 1
                xml = xml + f'<node ID="{id}" '

                # graying completed
                complete = get_attr(line, '_complete')
                if complete == 'true':
                    xml = xml + f'BACKGROUND_COLOR="#cccccc" '

                # copying text attribute
                text = get_attr(line, 'text')
                if text != '':
                    xml = xml + f'TEXT="{text}" '

                # children of level 1 are placed in some order
                if level == 1:
                    note = get_attr(line, '_note')
                    if note[:len('right')] == 'right':
                        xml = xml + f'POSITION="right" '
                        right_nodes = right_nodes + 1
                    elif note[:len('left')] == 'left' \
                            or (complete == 'true' and MOVE_COMPLETED_LEFT) \
                            or left_nodes < right_nodes:
                        xml = xml + f'POSITION="left" '
                        left_nodes = left_nodes + 1
                    else:
                        xml = xml + f'POSITION="right" '
                        right_nodes = right_nodes + 1

                if line[-1*len('/>'):] == '/>':                   # closing of a tag inline
                    xml = xml + '/>\n'                  # we do the same
                else:                                   # not closed tag
                    xml = xml + '>\n'                   # we do the same
                    level = level + 1                   # increse level for the next node


            elif line[:len('</outline>')] == '</outline>':             # closing of a tag in a separate line
                xml = xml + '</node>\n'                 # we do the same
                level = level - 1                       # decresed level of the next node

            else:
                pass

    return xml


def write_fm_file(wf_file):
    # translating from opml to mm format
    xml = read_wf_file(wf_file)

    # writing FreeMind .mm file
    fm_file = wf_file + ".mm"
    fm_file = fm_file.replace(' ', '_')  # avoiding spaces in file names
    with open(fm_file, 'w', encoding='utf_8') as fm:
        fm.write(xml)

    return fm_file


def on_created(event):
    time.sleep(2)
    fm_file = write_fm_file(event.src_path)
    time.sleep(2)
    # Mind Map program start
    if MINDMAP_AUTOSTART:
        cmdline = '"' + os.path.expanduser(MINDMAP_COMMAND) + '" ' + fm_file
        os.system(cmdline)


def on_modified(event):
    time.sleep(2)
    fm_file = write_fm_file(event.src_path)
    time.sleep(2)
    # Mind Map program start
    if MINDMAP_AUTOSTART:
        cmdline = '"' + os.path.expanduser(MINDMAP_COMMAND) + '" ' + fm_file
        os.system(cmdline)


def main():
    working_dir = os.path.expanduser(WORKING_DIR)  # adapting path string to OS

    if WATCHDOG:

        my_event_handler = PatternMatchingEventHandler(['WF*.opml'], None, True, True)
        my_event_handler.on_created = on_created
        my_event_handler.on_modified = on_modified
        my_observer = Observer()
        my_observer.schedule(my_event_handler, working_dir, recursive=True)
        my_observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()
    else:
        # for all WF*.opml files in the directory
        wf_files = glob.glob(working_dir+'WF*.opml')
        for wf_file in wf_files:
            fm_file = write_fm_file(wf_file)

        # Mind Map program start
        if MINDMAP_AUTOSTART:
            cmdline = '"' + os.path.expanduser(MINDMAP_COMMAND) + '" ' + fm_file
            os.system(cmdline)


if __name__ == "__main__":
    main()
