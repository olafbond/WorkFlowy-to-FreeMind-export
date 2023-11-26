# WorkFlowy-to-FreeMind-export
This Python macro translates WorkFlowy's *.opml files in a given directory into Freemind's *.mm files.
2023-11-26 - first release.

1. Install Free Mind (or use any other software which supports *.mm format)
2. Open Python code and define working_dir constant. This directory would be monitored for WF*.opml files and new *.mm files would apper there too.
3. Open a WF node which contains your data for visualization.
4. You may move the first level of subnodes by words 'left' or 'right' in a note field. Other nodes would be placed automatically.
5. Export your node into the dedicated directory in opml format.
6. Start Python macros. A new *.mm file should appear in the same directory.
7. Open mm file in Free Mind (or other software).
