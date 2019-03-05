import re, shutil, os, subprocess, time, stat

watch_dir = os.path.abspath("Z:\\_EXR_IN")
server_dir = os.path.abspath("Z:\\monster")
trans_dir = os.path.join(server_dir, "ame")

# server_dir = os.path.abspath("E:\\test\\Animation_In\\monster")
# trans_dir = os.path.abspath("E:\\Dropbox (BigBangBoxSL)\\PROYECTOS\\My preschool monster serie\\PRODUCCION\\Editorial\\FTG\\__EXR_to_ProRes4444XQ")

# dest_dir = os.path.join(watch_dir, 'monster')
dest_dir = server_dir
ame = os.path.abspath("C:\\Program Files\\Adobe\\Adobe Media Encoder CC 2019\\Adobe Media Encoder.exe")
ext = '.exr'

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

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
    epi_path = os.path.join(dest_dir, f'S{season}\\S{season}E{episode}\\shots\\exr')
    
    ver = f'V{pad_zero(ver_finder(epi_path), 3)}'
    shot_ver = f'{shot_base}_{ver}'

    shot_path = os.path.join(dest_dir, f'{epi_path}\\{shot_ver}')
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
    
    print("added versions")
  
    for img in os.listdir(exr_dir): 
        img_source = os.path.join(exr_dir, img)
        shutil.move(img_source, shot_path)
        print("moved to shot dir:", img)

    shutil.rmtree(curr_dir, onerror=remove_readonly)

    for img in os.listdir(shot_path):
        img_path = os.path.join(shot_path, img)
        shutil.copy2(img_path, trans_dir)
        print("copied to ame:", img)
    
    

subprocess.Popen(ame)
            

    

    # rename = f"monster_S{season}E{episode}_SQ{sequence}_SH{shot}.mov"
    # shutil.move(os.path.join(watch_dir, contents), os.path.join(rename_dir, rename))

