#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Este programa está em desenvolvimento sem versão. Será desenvolvido com suporte a 
Windows e Linux.
'''

import sys, os, subprocess
import sys
from PyQt5.QtWidgets import (QApplication, 
							QWidget, 
							QPushButton, 
							QLineEdit, 
                            QHBoxLayout, 
                            QMessageBox,
                            QGroupBox,
                            QVBoxLayout,
                            QRadioButton,
                            QGridLayout,
                            )
from PyQt5.QtGui import QIcon
'''
from PyQt5 import (
					QtWidgets, 
					QtGui, 
					QtCore,
					)
'''


__version__ = '2020-12-31'

dir_of_executable = os.path.dirname(os.path.realpath(__file__))
dir_local_lib = os.path.abspath(os.path.join(dir_of_executable, 'lib'))
sys.path.insert(0, dir_local_lib)
os.chdir(dir_of_executable)
from lib import utils, epsxe_config

config = utils.SetUserConfig()
if utils.KERNEL_TYPE == 'Windows':
	url_epsxe_zip = 'http://www.epsxe.com/files/ePSXe205.zip'
	path_epsxe_zip_file = os.path.abspath(os.path.join(config.dir_cache, 'ePSXe205.zip'))
elif utils.KERNEL_TYPE == 'Linux':
	url_epsxe_zip = 'http://www.epsxe.com/files/ePSXe205linux.zip'
	path_epsxe_zip_file = os.path.abspath(os.path.join(config.dir_cache, 'ePSXe205linux.zip'))

class Window(QWidget):
	'''
	https://medium.com/@wilfilho/pyqt5-o-fantastico-mundo-das-guis-62914b1b39c1
	https://medium.com/@wilfilho/conhecendo-o-coracao-e-as-arterias-do-pyqt5-22ba4187531
	'''
	def __init__(self, parent=None):
		super(Window, self).__init__()
		self.window_icon = os.path.abspath(os.path.join(dir_of_executable, 'imgs', 'epsxe.png')) 
		self.setWindowIcon(QIcon())
		self.setWindowTitle('Epsxe-Qt-Gui')
		self.resize(400, 480)
		self.set_buttons()
		self.text = ''
		self.title_info = ''


	def set_buttons(self):
		
		# Botões com caixa de seleção.
		self.option_download = QRadioButton("Baixar")
		self.option_download.setChecked(True)
		self.option_installer = QRadioButton("Instalar")
		self.option_uninstall = QRadioButton("Desinstalar")

		# Box para Widgets
		self.groupbox = QGroupBox("Selecione uma opção")

		# Layout options.
		self.layout_options = QVBoxLayout()
		self.layout_options.addWidget(self.option_download)
		self.layout_options.addWidget(self.option_installer)
		self.layout_options.addWidget(self.option_uninstall)
		self.groupbox.setLayout(self.layout_options)

		# Botão OK.
		self.button_ok = QPushButton('OK', self)
		self.button_ok.clicked.connect(self.run)

		# Layout para o botão OK.
		self.layout_widgets_click = QHBoxLayout()
		self.layout_widgets_click.addWidget(self.button_ok)

		# Main Layout
		self.layout_master = QVBoxLayout()
		#self.layout_master.addLayout(self.layout_widgets_click)
		self.layout_master.addWidget(self.groupbox)
		self.layout_master.addLayout(self.layout_widgets_click)
		self.setLayout(self.layout_master)		

		# Botão sair.
		self.buttonExit = QPushButton('Sair', self)
		self.buttonExit.clicked.connect(self.click_exit_button)
		self.layout_master.addWidget(self.buttonExit)
		self.setLayout(self.layout_master)

	def run(self):
		if self.option_download.isChecked():
			self.download_epsxe()
			return
		elif self.option_installer.isChecked():
			epsxe_config.teste()
			self.text = 'Ação para instalar o programa.'
			self.title_info = 'Instalar'
		elif self.option_uninstall.isChecked():
			self.text = 'Ação para desinstalar o programa.'
			self.title_info = 'Desinstalar'

		self.messsage_box = QMessageBox.information(self, self.title_info, self.text)
		
	def download_epsxe(self):
		output = utils.downloader(url_epsxe_zip, path_epsxe_zip_file)
		if output == False:
			self.text = 'Falha no download.'
			self.title_info = 'Erro'
			self.messsage_box = QMessageBox.critical(self, self.title_info, self.text)
			return False
		else:
			self.text = 'Download Concluido com sucesso.'
			self.title_info = 'Download'
			self.messsage_box = QMessageBox.information(self, self.title_info, self.text)

	def click_exit_button(self):
		exit_msg = QMessageBox.question(
						self, 
						'MessageBox', 
						"Deseja sair?", 
						QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
						)

		if exit_msg == QMessageBox.Yes:
			print('QMessageBox.Yes: saindo')
			sys.exit()

root = QApplication(sys.argv)
app = Window()
app.show()
sys.exit(root.exec_())