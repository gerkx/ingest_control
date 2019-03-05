import re, shutil, os, subprocess, time
from unidecode import unidecode
from openpyxl import load_workbook

main_dir = os.path.abspath("E:\\test\\Audio_In")
watch_dir = os.path.join(main_dir, "_audio_in")
gen_dir = os.path.abspath("E:\\Dropbox (BigBangBoxSL)\\PROYECTOS\\My preschool monster serie\\PRODUCCION\\Editorial\\Audio\\generico\\ingles\\ninos")
walla_dir = os.path.join(gen_dir, "wallas")
trama_dir = os.path.join(watch_dir, 'S01')
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
    curr_file = os.path.join(watch_dir, contents)
    if not os.path.isdir(curr_file):

        trama = re.search(r'cap\d{2}', contents, re.IGNORECASE)
        walla = re.search(r'walla', contents, re.IGNORECASE)
        nino = re.search(r'ninos', contents, re.IGNORECASE)

        if walla is not None:
            if os.path.isfile(os.path.join(walla_dir, contents)):
                continue
            shutil.move(curr_file, os.path.join(walla_dir, "ingles"))
            

        if trama is not None:
            epiNum = re.search(r'\d{2}', trama.group(0), re.IGNORECASE)
            epi = trama.group(0)[epiNum.start(0):epiNum.end(0)]
            title = unidecode(sheet[f'{col}{str(int(epi)+2)}'].value).lower().split(' ', 1)[0]
            
            file_path = os.path.join(trama_dir, f'epi{pad_zero(epi, 3)}_{title}\\voz\\ingles')
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            shutil.move(curr_file, file_path)

        # if ninos is not None and trama is None:

    


        

        
    


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
