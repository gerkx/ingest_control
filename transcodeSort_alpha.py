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
LOG_FILENAME = f'Logs\\AMEalpha_{year}{month}{day}{hour}{minute}{second}.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

spread_sheet = os.path.abspath("E:\\Dropbox (BigBangBoxSL)\\PROYECTOS\\My preschool monster serie\\PRODUCCION\\Script\\Storylines.xlsx")
wb = load_workbook(filename = spread_sheet)
sheet = wb["EPISODIOS"]
col = "I"

server_dir = os.path.abspath("Z:\\monster")
trans_dir = os.path.join(server_dir, "ame_alpha")
ftg_source = os.path.join(trans_dir, "Origen")
trans_out = os.path.join(trans_dir, "Salida")
edit_dir = os.path.abspath("E:\\Dropbox (BigBangBoxSL)\\PROYECTOS\\My preschool monster serie\\PRODUCCION\\Editorial\\FTG")


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

for contents in os.listdir(trans_out):
    log = '\n'
    ext = '.mov'
    qt = re.search(f'{ext}$', contents)
    
    if qt == None:
        continue

    se = re.search(r'S\d{2}E\d{2}', contents, re.IGNORECASE)
    sq = re.search(r'SQ\d{4}', contents, re.IGNORECASE)
    sh = re.search(r'SH\d{4}', contents, re.IGNORECASE)
    ver = re.search(r'_V\d{3}', contents, re.IGNORECASE)
    frame = re.search(r'.\d{4}.mov', contents, re.IGNORECASE)

    if not se or not sq or not sh or not ver:
        continue

    season = contents[se.start(0)+1:se.start(0)+3]
    episode = contents[se.start(0)+4:se.start(0)+6]
    title_base = unidecode(sheet[f'{col}{str(int(episode)+2)}'].value).lower().split(' ', 1)[0]        
    title = re.sub(r'[^\w\s]', '', title_base).lower()
    if len(title) < 1:
        title = ""
    else:
        title = f'_{title}'
    epi_path = os.path.join(server_dir, f'S{season}\\S{season}E{episode}{title}\\shots\\mov')
    if not os.path.exists(epi_path):
        os.makedirs(epi_path)

    current_dir = os.path.join(trans_out, contents)
    new_name = f'{contents[:frame.start(0)]}.mov'
    new_dir = os.path.join(epi_path, new_name)

    shutil.move(current_dir, new_dir)

    log += f'{now}: moved {contents} to: {epi_path}\n'
    
    edit_shot_dir = os.path.join(edit_dir, f'___S{season}\\S{season}E{episode}{title}\\Renders')
    if not os.path.exists(epi_path):
        os.makedirs(epi_path)
    shutil.copy2(new_dir, edit_shot_dir)
    log += f'{now}: copied {contents} to: {edit_shot_dir}\n'

    logging.info(log)


for folder in os.listdir(ftg_source):
    log = '\n'
    ftg_dir = os.path.join(ftg_source, folder)
    if not os.path.isdir(ftg_dir):
        continue
    
    for img in os.listdir(ftg_dir):
        exr = re.search(r'exr$', img, re.IGNORECASE)
        if exr == None:
            continue
        
        se = re.search(r'S\d{2}E\d{2}', img, re.IGNORECASE)
        sq = re.search(r'SQ\d{4}', img, re.IGNORECASE)
        sh = re.search(r'SH\d{4}', img, re.IGNORECASE)
        ver = re.search(r'_V\d{3}', img, re.IGNORECASE)

        if not se or not sq or not sh or not ver:
            continue

        season = img[se.start(0)+1:se.start(0)+3]
        episode = img[se.start(0)+4:se.start(0)+6]
        sequence = img[sq.start(0)+2:sq.start(0)+6]
        shot = img[sh.start(0)+2:sh.start(0)+6]
        version = img[ver.start(0)+2:ver.start(0)+5]
        title_base = unidecode(sheet[f'{col}{str(int(episode)+2)}'].value).lower().split(' ', 1)[0]        
        title = re.sub(r'[^\w\s]', '', title_base).lower()
        if len(title) < 1:
            title = ""
        else:
            title = f'_{title}'

        shot_name = f'S{season}E{episode}_SQ{sequence}_SH{shot}_alpha_V{version}'
        shot_path = os.path.join(server_dir, f'S{season}\\S{season}E{episode}{title}\\shots\\exr\\{shot_name}')        
        if not os.path.exists(shot_path):
            os.makedirs(shot_path)
        
        shutil.move(os.path.join(ftg_dir, img), os.path.join(shot_path, img))
        log += f'{now}: moved {img} to: {shot_path}\n'

    shutil.rmtree(ftg_dir, onerror=remove_readonly)
    log += f'{now}: deleted directory: {ftg_dir}\n'

    logging.info(log)


