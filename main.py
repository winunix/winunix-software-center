#!/usr/bin/python

import os
import json

moduleList = []

def listFolderByFolders(path):
	os.system('cd '+path+' && echo */ > modules.tmp')
	with open(path+'modules.tmp', 'r') as tmp:
		foldStr = tmp.read().replace('\n', '')
	foldArr = foldStr.split("/ ")
	os.system('cd '+path+' && rm modules.tmp')
	foldArr = map(lambda x: x.replace('/',''), foldArr)
	return foldArr

def listCSVFiles(path):
	os.system('cd '+path+' && echo *.csv > profiles.tmp')
	with open(path+'profiles.tmp', 'r') as tmp:
		fileStr = tmp.read().replace('\n', '')
	fileArr = fileStr.split(".csv ")
	fileArr = map(lambda x: x.replace('.csv',''), fileArr)
	os.system('cd '+path+' && rm profiles.tmp')
	return fileArr

def generateProfileBox():
	profiles = listCSVFiles('./profiles/')
	isChecked = 'TRUE'
	frag = ''
	for profile in profiles:
		frag += isChecked+' "'+profile+'" \\\n'
		if(isChecked == 'TRUE'):
			isChecked = 'FALSE'
	boxProfile = """perfil=$(
	zenity --list --radiolist --title="Perfis" --text="Selecione o perfil" \\
	--column="" --column="Perfil" --width=200 --height=200 --separator=':' \\
	"""+frag+') && echo $perfil > selected.tmp'
	os.system(boxProfile)

def getListProfile():
	generateProfileBox()
	with open('selected.tmp', 'r') as tmp:
		profile = tmp.read().replace('\n', '')
	os.system('rm selected.tmp')
	with open('./profiles/'+profile+'.csv') as tmp:
		selecteds = tmp.read().split('\n')
	return selecteds

def getListModules():
	global moduleList
	path = './modules/'
	modules = listFolderByFolders(path)
	modArr = []
	for module in modules:
		filename = path+module+'/manifest.json'
		if os.path.isfile(filename):
			with open(filename, 'r') as tmp:
				manifest = tmp.read()
			maniArr = json.loads(manifest)
			maniArr['name'] = maniArr['name'].replace(' ', '')
			modArr.append(maniArr)
	moduleList = modArr
	return modArr

def generateAppsBox():
	selecteds = getListProfile()
	frag = ''
	for module in getListModules():
		isChecked = 'FALSE'
		for sel in selecteds:
			if sel == module['name']:
				isChecked = 'TRUE'
				break
		frag += isChecked+' "'+module['name']+'" "'+module['description']+'" \\'
	boxApps = """softs=$(zenity --list --checklist \\
	--title="Pacotes a ser instalados" \\
	--text="lista de pacotes" --column="" --column="Pacote" \\
	--column="Descricao" --width=700 --height=400 --separator=':' \\
	"""+frag+"""
	) 2>/dev/null && echo $softs > apps.tmp"""
	os.system(boxApps)

generateAppsBox()
with open('apps.tmp', 'r') as tmp:
	modStr = tmp.read().replace('\n', '')
modArr = modStr.split(":")
os.system('rm apps.tmp')
for mod in moduleList:
	if mod['name'] in modArr:
		os.system('cd ./modules/'+mod['name']+'/ && ./install')
