#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import json

module_list = []


def list_folder_by_folders(path):
    os.system('cd '+path+' && echo */ > modules.tmp')
    with open(path+'modules.tmp', 'r') as tmp:
        fold_str = tmp.read().replace('\n', '')
    fold_arr = fold_str.split("/ ")
    os.system('cd '+path+' && rm modules.tmp')
    fold_arr = map(lambda x: x.replace('/', ''), fold_arr)
    return fold_arr


def list_csv_files(path):
    os.system('cd '+path+' && echo *.csv > profiles.tmp')
    with open(path+'profiles.tmp', 'r') as tmp:
        file_str = tmp.read().replace('\n', '')
    file_arr = file_str.split(".csv ")
    file_arr = map(lambda x: x.replace('.csv', ''), file_arr)
    os.system('cd '+path+' && rm profiles.tmp')
    return file_arr


def generate_profile_box():
    profiles = list_csv_files('./profiles/')
    is_checked = 'TRUE'
    frag = ''
    for profile in profiles:
        frag += is_checked+' "'+profile+'" \\\n'
        if(is_checked == 'TRUE'):
            is_checked = 'FALSE'
    box_profile = """perfil=$(
	zenity --list --radiolist --title="Perfis" --text="Selecione o perfil" \\
	--column="" --column="Perfil" --width=300 --height=400 --separator=':' \\
	"""+frag+') && echo $perfil > selected.tmp'
    os.system(box_profile)


def get_list_profile():
    generate_profile_box()
    with open('selected.tmp', 'r') as tmp:
        profile = tmp.read().replace('\n', '')
    os.system('rm selected.tmp')
    with open('./profiles/'+profile+'.csv') as tmp:
        selecteds = tmp.read().split('\n')
    return selecteds


def get_list_modules():
    global module_list
    path = './modules/'
    modules = list_folder_by_folders(path)
    mod_arr = []
    for module in modules:
        filename = path+module+'/manifest.json'
        if os.path.isfile(filename):
            with open(filename, 'r') as tmp:
                manifest = tmp.read()
            mani_arr = json.loads(manifest)
            mani_arr['name'] = mani_arr['name'].replace(' ', '')
            mod_arr.append(mani_arr)
    module_list = mod_arr
    return mod_arr


def generate_apps_box():
    selecteds = get_list_profile()
    frag = ''
    for module in get_list_modules():
        is_checked = 'FALSE'
        for sel in selecteds:
            if sel == module['name']:
                is_checked = 'TRUE'
                break
        frag += is_checked+' "'+module['name'] + \
            '" "'+module['description']+'" \\'
    box_apps = """softs=$(zenity --list --checklist \\
	--title="Pacotes a ser instalados" \\
	--text="lista de pacotes" --column="" --column="Pacote" \\
	--column="Descricao" --width=700 --height=400 --separator=':' \\
	"""+frag+"""
	) 2>/dev/null && echo $softs > apps.tmp"""
    os.system(box_apps.encode("utf-8"))


def progress(title, pulse=False):
    if (pulse):
        return " | zenity --progress --pulsate --no-cancel --auto-close --text=\"Espere um pouco...\" --title=\"Processando "+title+"\" --width=450"
    else:
        return " | zenity --progress --no-cancel --auto-close --text=\"Espere um pouco...\" --title=\"Processando "+title+"\" --width=450"


generate_apps_box()
with open('apps.tmp', 'r') as tmp:
    modStr = tmp.read().replace('\n', '')
mod_arr = modStr.split(":")
os.system('rm apps.tmp')
for mod in module_list:
    pulse = True if ( ('pulse' in mod.keys()) and (mod['pulse'] == 'true') ) else False
    if mod['name'] in mod_arr:
        if 'license' in mod:
            isAgreed = os.system( 'zenity --text-info --title "Licenca %s" --checkbox="Eu aceito os termos" --filename="%s" --width=550 --height=400' % (mod['name'], mod['license']) ) == 0
        else:
            isAgreed = True
        if isAgreed:
            os.system('cd ./modules/'+mod['name'] +
                      '/ && ./install'+progress(mod['name'], pulse))
        else:
            os.system('cd ./modules/'+mod['name'] +
                      '/ && ./install -u'+progress(mod['name'], pulse))
    else:
        os.system('cd ./modules/'+mod['name'] +
                  '/ && ./install -u'+progress(mod['name'], pulse))
os.system("pkexec /usr/wx-center/superuser.sh 'autoremove'" +
          progress('Superusuário', True))
