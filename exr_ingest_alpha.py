import re, shutil, os, subprocess, time, stat, logging
from datetime import datetime
from unidecode import unidecode
from openpyxl import load_workbook

def pad_zero(num, pad):
    num = str(num)
    while len(num) < pad:
        num = "0" + num
    return num

now = datetime.now()
year = pad_zero(now.year,2)
month = pad_zero(now.month,2)
day = pad_zero(now.day,2)
hour = pad_zero(now.hour,2)
minute = pad_zero(now.minute,2)
second = pad_zero(now.second,2)
LOG_FILENAME = f'Logs\\EXR_alpha_{year}{month}{day}{hour}{minute}{second}.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

spread_sheet = os.path.abspath("E:\\Dropbox (BigBangBoxSL)\\PROYECTOS\\My preschool monster serie\\PRODUCCION\\Script\\Storylines.xlsx")
wb = load_workbook(filename = spread_sheet)
sheet = wb["EPISODIOS"]
col = "I"

watch_dir = os.path.abspath("Z:\\_EXR_IN_alpha")
server_dir = os.path.abspath("Z:\\monster")
trans_dir = os.path.join(server_dir, "ame_alpha")

dest_dir = server_dir
ame = os.path.abspath("C:\\Program Files\\Adobe\\Adobe Media Encoder CC 2019\\Adobe Media Encoder.exe")

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)



def ver_finder(path):
    if not os.path.exists(path):
        return 1
    prev_ver = 0

    for shots in os.listdir(path):
        ver = shots.find(shot_base)+1
        prev_ver += ver
    return prev_ver + 1

for contents in os.listdir(watch_dir):
    log = '\n'
    curr_dir = os.path.join(watch_dir, contents)

    if not os.path.isdir(curr_dir):
        continue
    
    se = re.search(r'S\d{2}E\d{2}', contents, re.IGNORECASE)
    sq = re.search(r'SQ\d{4}', contents, re.IGNORECASE)
    sh = re.search(r'SH\d{4}', contents, re.IGNORECASE)
    verPadTwo = re.search(r'_v\d{2}', contents, re.IGNORECASE)
    verPadThree = re.search(r'_v\d{3}', contents, re.IGNORECASE)

    if not se or not sq or not sh:
        continue

    season = contents[se.start(0)+1:se.start(0)+3]
    episode = contents[se.start(0)+4:se.start(0)+6]
    sequence = contents[sq.start(0)+2:sq.start(0)+6]
    shot = contents[sh.start(0)+2:sh.start(0)+6]
    print(season, episode, shot)

    title_base = unidecode(sheet[f'{col}{str(int(episode)+2)}'].value).lower().split(' ', 1)[0]        
    title = re.sub(r'[^\w\s]', '', title_base).lower()
    if len(title) < 1:
        title = ""
    else:
        title = f'_{title}'
    
    shot_base = f'S{season}E{episode}_SQ{sequence}_SH{shot}_alpha'
    epi_path = os.path.join(dest_dir, f'S{season}\\S{season}E{episode}{title}\\shots\\exr')
    
    if verPadTwo and not verPadThree:
        ver = f'V{pad_zero(verPadTwo.group(0)[2:], 3)}'
    elif verPadThree:
        ver = f'V{pad_zero(verPadThree.group(0)[2:], 3)}'
    else:
        ver = f'V{pad_zero(ver_finder(epi_path), 3)}'
    shot_ver = f'{shot_base}_{ver}'
 
    shot_path = os.path.join(dest_dir, f'{epi_path}\\{shot_ver}')
    if not os.path.exists(shot_path):
        os.makedirs(shot_path)
        log += f'{now}: created directory: {shot_path}\n'
    
    exr_dir = f'{curr_dir}\\exr'
    
    for img in os.listdir(exr_dir):
        ext = '.exr'
        exr = re.search(f'{ext}$', img)
        if exr == None:
            continue
        elif re.search(r'_v\d{3}', img, re.IGNORECASE):
            continue
        else:
            img_shot = re.search(r'SH\d{4}', img, re.IGNORECASE)
            name_ver = f'{img[:img_shot.end(0)]}_alpha_{ver}{img[img_shot.end(0):]}'
            orig_file = os.path.join(exr_dir, img)
            new_file = os.path.join(exr_dir, name_ver)
            os.rename(orig_file, new_file)
            log += f'{now}: renamed {img} to: {name_ver}\n'
  
    for img in os.listdir(exr_dir): 
        img_source = os.path.join(exr_dir, img)
        shutil.move(img_source, trans_dir)
        log += f'{now}: moved {img} to: {trans_dir}\n'

    shutil.rmtree(curr_dir, onerror=remove_readonly)
    log += f'{now}: deleted directory: {curr_dir}\n'

    logging.info(log)

subprocess.Popen(ame)
