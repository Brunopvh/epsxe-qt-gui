#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import re
import getpass
import shutil
import tempfile
import urllib.request
import progressbar
from pathlib import Path

app_name = 'epsxe-gui'

# Default
CRed = '\033[0;31m'
CGreen = '\033[0;32m'
CYellow = '\033[0;33m'
CBlue = '\033[0;34m'
CWhite = '\033[0;37m'
CReset = '\033[m'

# Strong
CSRed = '\033[1;31m'
CSGreen = '\033[1;32m'
CSYellow = '\033[1;33m'
CSBlue = '\033[1;34m'
CSWhite = '\033[1;37m'

KERNEL_TYPE = platform.system()

try:
	COLUMNS = int(os.get_terminal_size()[0])
except:
	COLUMNS = int(45)

def print_line():
	print('-' * COLUMNS)

#=====================================================#

def mkdir(path):
		if path == '':
			return False
		try:
			if not os.path.exists(path):
				print(f'Criando diretório ... {path}')
				os.makedirs(path, 0o700)
				return True
		except Exception as err:
			print(err)
			return False
		if not os.access(path, os.W_OK):
			print("[!] Você não tem permissão de escrita em: {0}".format(path))
			return False
		return True

#=====================================================#

def rmdir(path):
	if not path:
		return

	try:
		print(f'Apagando ... {path}')
		shutil.rmtree(path)
	except:
		print(f'{CRed}Erro ao tentar apagar ... {path}{CReset}')
		return False
	else:
		return True

#=====================================================#

def read_file(file: str) -> list:
	'''
	Ler um arquivo e retornar as linhas em forma de lista.
	'''
	if os.path.isfile(file) == False:
		print(f'read_file: Erro arquivo não encontrado.')
		return False

	try:
		with open(file, 'rt') as f:
			lines = f.read().split('\n')
	except:
		print(f'read_file: Erro')
		return []
	else:
		return lines

#=====================================================#

def write_file(content: list, file: str) -> bool:
	"""
	Recebe um arquivo seguido de uma lista, grava o contéudo da lista
	no arquivo que será aberto em modo 'w'. 
	
	OBS: 
       - Quebras de linha são adicionadas ao fim de cada elemento da lista.
       - Se o arquivo 'file' já existir a função será encerrada.
	"""
	
	print(f'Gravando dados no arquivo ... {file} ', end='')
	try:
		with open(file, 'w+') as f:
			for L in content:
				if L != '':
					f.write(f'{L}\n')
	except:
		print('write_file: Erro')
		return False
	else:
		print('OK')
		return True

#=====================================================#

def string_in_file(string: str, file: str, case_sensitive=True) -> list:
	'''
	Verifica se uma string existe em um arquivo de texto e retorna as ocorrências
	encontradas no arquivo, se a string não existir nas linhas do arquivo, retorna
	uma lista vazia [].
	'''
	if os.path.isfile(file) == False:
		print(f'string_in_file: Erro')
		return []

	try:
		content = read_file(file)
	except:
		print('string_in_file: Erro')
		return []
	else:
		if content == False:
			print('string_in_file: Erro')
			return []

	ContentMath = []
	if case_sensitive == False: 
		string = string.lower()

	RegExp = re.compile(r'{}'.format(string))
	for line in content:
		NewLine = line
		if case_sensitive == False:
			NewLine = line.lower()

		if (RegExp.findall(NewLine) != []):
			ContentMath.append(NewLine)
	return ContentMath
			
#=====================================================#

user_agents = [
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
]

user_agent = user_agents[0]

class DowProgressBar():
	'''
	https://stackoverflow.com/questions/37748105/how-to-use-progressbar-module-with-urlretrieve
	'''
	def __init__(self):
		self.pbar = None

	def __call__(self, block_num, block_size, total_size):
		if not self.pbar:
			self.pbar = progressbar.ProgressBar(maxval=total_size)
			self.pbar.start()

		downloaded = block_num * block_size
		if downloaded < total_size:
			self.pbar.update(downloaded)
		else:
			self.pbar.finish()

def downloader(url: str, output_file: str) -> bool:
	'''
	Retorna True se o download for executado com suscesso, ou False caso o download falhe.
	'''
	# https://homepages.inf.ed.ac.uk/imurray2/code/hacks/urlsize
	# https://stackoverflow.com/questions/37748105/how-to-use-progressbar-module-with-urlretrieve
	# https://www.programmersought.com/article/80002135225/
	# curl -i HEAD url
	RegExp = re.compile(r'^http|ftp|www')
	if (RegExp.findall(url) == []):
		print(f'downloader: Falha informe um url válido')
		return

	print_line()
	print(f'Conectando ... {url}')
	req = urllib.request.Request(
	    		url, 
	    		data=None, 
	    		headers={
					'User-Agent': user_agent 
					}	
				)
	try:
		response = urllib.request.urlopen(req)
	except:
		print(f'downloader: Falha')
		return False
	else:	
		file_online_info = response.info()
		num_bytes = int(file_online_info.get('content-length'))
		num_megabytes = float(num_bytes / 1048576)	
		type_file = file_online_info.get('content-type')
		
		if num_bytes and type_file:
			print('{:.2f}MB | {}'.format(num_megabytes, type_file))

		urllib.request.urlretrieve(url, output_file, DowProgressBar())
		return True

#=====================================================#

class SetUserConfig:

	def __init__(self, kernel_type=platform.system()):
		self.dir_home = Path.home()
		self.kernel_type = kernel_type
		if self.kernel_type == 'Linux':
			self.dir_bin = os.path.abspath(os.path.join(self.dir_home, '.local', 'bin'))
			self.dir_desktop_links = os.path.abspath(os.path.join(self.dir_home, '.local', 'share', 'applications'))
			self.dir_cache = os.path.abspath(os.path.join(self.dir_home, '.cache', app_name))
			self.dir_config = os.path.abspath(os.path.join(self.dir_home, '.config', app_name))
			self.file_config = os.path.abspath(os.path.join(self.dir_config, f'{app_name}.conf'))
		elif self.kernel_type == 'Windows':
			self.dir_config = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Roaming', app_name))
			self.dir_cache = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'LocalLow', app_name))
			self.file_config = os.path.abspath(os.path.join(self.dir_config, '{}.conf'.format(app_name)))
			self.file_config = os.path.abspath(os.path.join(self.dir_config, f'{app_name}.conf'))	
			self.dir_bin = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Local', 'Programs', app_name))	
			self.dir_desktop_links = ''

		self.file_temp = tempfile.NamedTemporaryFile(delete=True).name
		# self.dir_temp = tempfile.TemporaryDirectory().name
		if self.kernel_type == 'Linux':
			self.dir_temp = os.path.abspath(os.path.join('/tmp', f'{app_name}-{getpass.getuser()}'))
		elif self.kernel_type == 'Windows':
			self.dir_temp = os.path.abspath(os.path.join('C:', f'{app_name}-{getpass.getuser()}'))

		self.user_info = {
			'home': self.dir_home,
			'cache': self.dir_cache,
			'config': self.dir_config,
			'bin': self.dir_bin,
			'desktop_links': self.dir_desktop_links,
			'dir_temp': self.dir_temp,
		}

		for key in self.user_info:
			d = self.user_info[key]
			if os.path.isdir(d) == False:
				mkdir(d)
		
	# Getter para kernel_type
	@property
	def kernel_type(self):
		return self._kernel_type

	# Setter para kernel_type
	@kernel_type.setter
	def kernel_type(self, kernel):
		if isinstance(kernel, str):
			if (kernel == 'Windows') or (kernel == 'Linux'):
				self._kernel_type = kernel
			else:
				sefl._kernel_type = None
		else:
			self._kernel_type = None

	
	def get_user_info(self):
		return self.user_info

	def config_bashrc(self):
		'''
		Configurar o arquivo .bashrc do usuário para inserir o diretório ~/.local/bin
		na variável de ambiente $PATH. Essa configuração será abortada caso ~/.local/bin já 
		exista em ~/.bashrc.
		'''
		if self.kernel_type != 'Linux':
			print(f'{CRed}Seu sistema não é Linux.{CReset}')
			return False

		# Verificar se ~/.local/bin já está no PATH do usuário atual.
		user_local_path = os.environ['PATH']
		if self.dir_bin in user_local_path:
			return True

		file_bashrc = os.path.abspath(os.path.join(self.dir_home, '.bashrc'))
		file_bashrc_backup = os.path.abspath(os.path.join(self.dir_home, f'.bashrc.pre-{app_name}'))
		if os.path.isfile(file_bashrc_backup) == False:
			shutil.copyfile(file_bashrc, file_bashrc_backup)

		content_bashrc = string_in_file('^export PATH=', file_bashrc)
		if (content_bashrc != []) and (self.dir_bin in content_bashrc[0]):
			return True

		content_bashrc = read_file(file_bashrc)
		RegExp = re.compile(r'^export PATH=')
		num = 0
		for line in content_bashrc:
			if (RegExp.findall(line) != []):
				line = f'# {line}'
				content_bashrc[num] = line
				print(line)
			num += 1
				
		NewUserPath = f'export PATH={self.dir_bin}:{user_local_path}'
		content_bashrc.append(NewUserPath)
		os.remove(file_bashrc)
		write_file(content_bashrc, file_bashrc)




	


