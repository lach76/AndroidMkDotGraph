#!/usr/bin/env python
import os
import sys

module_dependency_dict = {}

def get_library_name(list_item, target):
    result = " ".join(list_item).replace('\\','')
    result = result.replace(":=", '')
    resultlist = result.split()
    return " ".join(resultlist[1:])

def parse_and_store(fullname, content):
    fullpath = os.path.dirname(fullname)
    dirname = os.path.basename(fullpath)
    shared_lib_list = []
    local_lib_list = []
    found_shared = False;
    found_local = False;
    for line in content:
        line = line.strip()
        if line.startswith("LOCAL_SHARED_LIBRARIES"):
            found_shared = True

        if found_shared:
            shared_lib_list.append(line)
            if not line.endswith('\\'):
                found_shared = False

        if line.startswith("LOCAL_MODULE") and not line.startswith("LOCAL_MODULE_TAG"):
            found_local = True

        if found_local:
            local_lib_list.append(line)
            if not line.endswith('\\'):
                found_local = False

    # shared lib diagnostic
    shared_libs = get_library_name(shared_lib_list, "LOCAL_SHARED_LIBRARIES")
    local_libs = get_library_name(local_lib_list, "LOCAL_MODULE")

    return shared_libs, local_libs

def androidMKFiles(basefolder):
    global module_dependency_dict

    for root, dirs, files in os.walk(basefolder):
        for file in files:
            if (file.endswith('.mk')):
                full_name = os.path.join(root, file)
                with open(full_name) as f:
                    content = f.readlines()

                shared_libs, local_libs = parse_and_store(full_name, content)
                module_dependency_dict[local_libs] = shared_libs

if __name__ == "__main__":
    if len(sys.argv) > 1:
        default_path = sys.argv[1]
    else:
        default_path = './'

    androidMKFiles(default_path)
    colorlist = [
        "#5d8aa8", "#f0f8ff", "#e32636", "#efdecd", "#e52b50", 
        "#ff033e", "#9966cc", "#a4c639", "#f2f3f4", "#cd9575", "#915c83",
        "#faebd7", "#008000", "#8db600", "#fbceb1", "#00ffff", "#7fffd4",
        "#4b5320", "#e9d66b","#b2beb5","#87a96b","#ff9966","#a52a2a",
        "#fdee00","#6e7f80","#ff2052","#007fff","#f0ffff","#89cff0",
        "#a1caf1","#f4c2c2","#21abcd","#fae7b5","#ffe135","#848482",
        "#98777b","#bcd4e6","#9f8170","#f5f5dc","#ffe4c4","#3d2b1f",
        "#fe6f5e","#000000","#ffebcd","#318ce7","#ace5ee","#faf0be",
        "#0000ff","#a2a2d0","#6699cc","#0d98ba","#8a2be2","#8a2be2",
        "#de5d83","#79443b","#0095b6","#e3dac9","#cc0000","#006a4e",
        "#873260","#0070ff","#b5a642","#cb4154","#1dacd6","#66ff00",
        "#bf94e4","#c32148","#ff007f","#08e8de","#d19fe8","#f4bbff",
        "#ff55a3","#fb607f","#004225","#cd7f32","#a52a2a","#ffc1cc",
        "#e7feff","#f0dc82","#480607","#800020","#deb887","#cc5500",
        "#e97451","#8a3324","#bd33a4","#702963","#007aa5","#e03c31",
        "#536872","#5f9ea0","#91a3b0","#006b3c","#ed872d","#e30022",
        "#fff600","#a67b5b","#4b3621","#1e4d2b","#a3c1ad","#c19a6b",
        "#78866b","#ffff99","#ffef00","#ff0800","#e4717a","#00bfff",
        "#592720","#c41e3a","#00cc99","#ff0040","#eb4c42","#ff0038"\
        ]
    if (1):
        print "digraph {"
        print "    concentrage=true"
        print "    rankdir=LR"
        print "    bgcolor=\"#000000\""
        print "    splines=ortho"
        print "    decorate=true"
        print "    nodespe=0.01"
        print "    node [shape=box]"
        index = 0
        for key, value in module_dependency_dict.items():
            labelstr = key
            colorvalue = colorlist[index]
            index += 1
            print "    \"" + key + "\" [label=\"%s\", style=\"filled\", stype=\"box\",fontname=\"DejaVu Sans Mono\", fontsize=10, fillcolor=\"white\", color=\"%s\"]" % (labelstr, colorvalue)
            for module in value.split():
                edge_str = "    edge[color=\"%s\", penwidth=1]" % colorvalue
                if module_dependency_dict.has_key(module):
                    other_modules = module_dependency_dict[module]
                    if other_modules.find(key) >= 0:
                        edge_str = "    edge[color=\"%s\", penwidth=3]" % colorvalue
                else:
                    print "    \"" + module + "\" [label=\"%s\", style=\"filled\", stype=\"box\",fontname=\"DejaVu Sans Mono\", fontsize=10, fillcolor=\"#808080\", color=\"#FFFFFF\"]" % module
                print edge_str
                print "    \"" + key + "\" -> \"" + module + "\""

        print "}"

    if (0):
        print "graph {"
        print "    rankdir=LR;"
        for key, value in module_dependency_dict.items():
            items = value.split()
            newlist = []
            for item in items:
                newlist.append("\"" + item + "\"")

            print "    \"" + key + "\" -- { " + " ".join(newlist) + " };"

        print "}"
