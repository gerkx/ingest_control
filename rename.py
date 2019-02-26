import re, shutil, os

watch_dir = os.path.abspath("E:\\test\\Animation_In")
server_dir = os.path.abspath("Z:\\monster")
rename_dir = os.path.join(watch_dir, 'renamed')
ext = '.mov'
# contents = os.listdir(watchDir)

for contents in os.listdir(watch_dir):
    mov = re.search(f'{ext}$', contents)

    if mov == None:
        continue

    else:
        base = re.search('monster_(.+?).mov', contents, re.IGNORECASE).group(1)
        season = base[1:3]
        episode = base[4:6]
        sequence = base[9:13]
        shot = base[16:20]
        rename = f"monster_S{season}E{episode}_SQ{sequence}_SH{shot}.mov"
        shutil.move(os.path.join(watch_dir, contents), os.path.join(rename_dir, rename))