import re, shutil, os, subprocess, time

watch_dir = os.path.abspath("E:\\test\\Animation_In")
server_dir = os.path.abspath("Z:\\monster")
dest_dir = os.path.join(watch_dir, 'monster')
trans_dir = os.path.abspath("E:\\Dropbox (BigBangBoxSL)\\PROYECTOS\\My preschool monster serie\\PRODUCCION\\Editorial\\FTG\\__EXR_to_ProRes4444XQ")
ame = os.path.abspath("C:\\Program Files\\Adobe\\Adobe Media Encoder CC 2019\\Adobe Media Encoder.exe")
ext = '.exr'

def pad_zero(num, pad):
    num = str(num)
    while len(num) < pad:
        num = "0" + num
    return num

def ver_finder(path):
    if not os.path.exists(path):
        return 1
    prev_ver = 0

    for shots in os.listdir(path):
        ver = shots.find(shot_base)+1
        prev_ver += ver
    return prev_ver + 1

for contents in os.listdir(watch_dir):
    curr_dir = os.path.join(watch_dir, contents)

    if not os.path.isdir(curr_dir):
        continue
    
    se = re.search(r'S\d{2}E\d{2}', contents, re.IGNORECASE)
    sq = re.search(r'SQ\d{4}', contents, re.IGNORECASE)
    sh = re.search(r'SH\d{4}', contents, re.IGNORECASE)

    if not se or not sq or not sh:
        continue

    season = contents[se.start(0)+1:se.start(0)+3]
    episode = contents[se.start(0)+4:se.start(0)+6]
    sequence = contents[sq.start(0)+2:sq.start(0)+6]
    shot = contents[sh.start(0)+2:sh.start(0)+6]
    
    shot_base = f'S{season}E{episode}_SQ{sequence}_SH{shot}'
    epi_path = os.path.join(dest_dir, f'S{season}\\S{season}E{episode}\\Shots')
    
    ver = f'V{pad_zero(ver_finder(epi_path), 3)}'
    shot_ver = f'{shot_base}_{ver}'

    shot_path = os.path.join(dest_dir, f'{epi_path}\\{shot_ver}\\exr')
    if not os.path.exists(shot_path):
        os.makedirs(shot_path)
    
    exr_dir = f'{curr_dir}\\exr'
    
    for img in os.listdir(exr_dir):
        exr = re.search(f'{ext}$', img)
        if exr == None:
            continue
        elif re.search(r'_v\d{3}', img, re.IGNORECASE):
            continue
        else:
            img_shot = re.search(r'SH\d{4}', img, re.IGNORECASE)
            name_ver = f'{img[:img_shot.end(0)]}_{ver}{img[img_shot.end(0):]}'
            orig_file = os.path.join(exr_dir, img)
            new_file = os.path.join(exr_dir, name_ver)
            os.rename(orig_file, new_file)
            
            shutil.copy2(new_file, shot_path)
            shutil.copy2(new_file, trans_dir)
    
    shutil.rmtree(curr_dir)

subprocess.Popen(ame)
            

    

    # rename = f"monster_S{season}E{episode}_SQ{sequence}_SH{shot}.mov"
    # shutil.move(os.path.join(watch_dir, contents), os.path.join(rename_dir, rename))

