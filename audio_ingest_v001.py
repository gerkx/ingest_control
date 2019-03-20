import re, shutil, os, subprocess, time, logging
from datetime import datetime
from util import log, pad
from unidecode import unidecode
from openpyxl import load_workbook

now = datetime.now()
year = pad.two(now.year)
month = pad.two(now.month)
day = pad.two(now.day)
hour = pad.two(now.hour)
minute = pad.two(now.minute)
second = pad.two(now.second)
LOG_FILENAME = f'Logs\\audio_{year}{month}{day}{hour}{minute}{second}.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

main_dir = os.path.abspath("E:\\Dropbox (BigBangBoxSL)\\PROYECTOS\\My preschool monster serie\\PRODUCCION\\Editorial\\Audio")
watch_dir = os.path.join(main_dir, "_audio_in")
gen_dir = os.path.join(main_dir, "generico\\ingles")
walla_dir = os.path.join(gen_dir, "wallas")
trama_dir = os.path.join(main_dir, 'S01')
ninos_dir = os.path.join(gen_dir, "ninos")
season = 1

spread_sheet = os.path.abspath("E:\\Dropbox (BigBangBoxSL)\\PROYECTOS\\My preschool monster serie\\PRODUCCION\\Script\\Storylines.xlsx")
wb = load_workbook(filename = spread_sheet)
sheet = wb["EPISODIOS"]
col = "I"


def pad_zero(num, pad):
    num = str(num)
    while len(num) < pad:
        num = "0" + num
    return num

# def ver_finder(path):
#     if not os.path.exists(path):
#         return 1
#     prev_ver = 0

#     for shots in os.listdir(path):
#         ver = shots.find(shot_base)+1
#         prev_ver += ver
#     return prev_ver + 1

for contents in os.listdir(watch_dir):
    log = '\n'
    file_name = contents
    curr_file = os.path.join(watch_dir, file_name)
    if not os.path.isdir(curr_file):

        trama = re.search(r'cap\d{1}', file_name, re.IGNORECASE)
        walla = re.search(r'walla', file_name, re.IGNORECASE)
        nino = re.search(r'ninos', file_name, re.IGNORECASE)

        if walla is not None:
            if os.path.isfile(os.path.join(walla_dir, file_name)):
                continue
            shutil.move(curr_file, walla_dir)
            log += f'{log.now()}: moved {file_name} to: {walla_dir}\n'
            

        if trama is not None:
            pad_two = re.search(r'\d{2}', file_name, re.IGNORECASE)
            
            pad_one = re.search(r'\d{1}', file_name, re.IGNORECASE)
            
            if pad_two is None and pad_one is not None:
                orig_file = os.path.join(watch_dir, file_name)
                # print(file_name)
                epi = pad_zero(file_name[pad_one.start(0):pad_one.end(0)],2)
                cap = f'CAP{epi}'
                # print(cap)
                name_start = file_name[:trama.start(0)]
                name_end = file_name[trama.end(0):]
                file_name = f'{name_start}{cap}{name_end}'
                

                curr_file = os.path.join(watch_dir, file_name)
                os.rename(orig_file, curr_file)
            else:
                epi = file_name[pad_two.start(0):pad_two.end(0)]
            # print(file_name, epi)
            title_base = unidecode(sheet[f'{col}{str(int(epi)+2)}'].value).lower().split(' ', 1)[0]
            title = re.sub(r'[^\w\s]', '', title_base)
            file_path = os.path.join(trama_dir, f'epi{pad_zero(epi, 3)}_{title}\\voz\\ingles')
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            
            if os.path.isfile(os.path.join(file_path, file_name)):
                orig_file = os.path.join(watch_dir, file_name)
                base_name = file_name.split(".")
                new_ver = year[2:]+month+day
                file_name = f'{base_name[0]} {new_ver}.{base_name[1]}'
                
                curr_file = os.path.join(watch_dir, file_name)
                os.rename(orig_file, curr_file)

            shutil.move(curr_file, file_path)
            log += f'{now}: moved {contents} to: {file_path}\n'

        # if ninos is not None and trama is None:
        
        logging.info(log)


        

        
    


    # if not se or not sq or not sh:
    #     continue

    # season = contents[se.start(0)+1:se.start(0)+3]
    # episode = contents[se.start(0)+4:se.start(0)+6]
    # sequence = contents[sq.start(0)+2:sq.start(0)+6]
    # shot = contents[sh.start(0)+2:sh.start(0)+6]
    
    # shot_base = f'S{season}E{episode}_SQ{sequence}_SH{shot}'
    # epi_path = os.path.join(dest_dir, f'S{season}\\S{season}E{episode}\\Shots')
    
    # ver = f'V{pad_zero(ver_finder(epi_path), 3)}'
    # shot_ver = f'{shot_base}_{ver}'

    # shot_path = os.path.join(dest_dir, f'{epi_path}\\{shot_ver}\\exr')
    # if not os.path.exists(shot_path):
    #     os.makedirs(shot_path)
    
    # exr_dir = f'{curr_dir}\\exr'
    
    # for img in os.listdir(exr_dir):
    #     exr = re.search(f'{ext}$', img)
    #     if exr == None:
    #         continue
    #     elif re.search(r'_v\d{3}', img, re.IGNORECASE):
    #         continue
    #     else:
    #         img_shot = re.search(r'SH\d{4}', img, re.IGNORECASE)
    #         name_ver = f'{img[:img_shot.end(0)]}_{ver}{img[img_shot.end(0):]}'
    #         orig_file = os.path.join(exr_dir, img)
    #         new_file = os.path.join(exr_dir, name_ver)
    #         os.rename(orig_file, new_file)
            
    #         shutil.copy2(new_file, shot_path)
    #         shutil.copy2(new_file, trans_dir)
    
    # shutil.rmtree(curr_dir)

            

    

    # rename = f"monster_S{season}E{episode}_SQ{sequence}_SH{shot}.mov"
    # shutil.move(os.path.join(watch_dir, contents), os.path.join(rename_dir, rename))
