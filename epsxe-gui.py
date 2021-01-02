#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Este programa está em desenvolvimento sem versão. Será desenvolvido com suporte a 
Windows e Linux.
'''

import sys, os, subprocess
import sys
from PyQt5.QtWidgets import (
							QApplication, 
							QAction,
							qApp,
							QFrame,
                            QMainWindow,
							QWidget, 
							QPushButton, 
							QLineEdit,
							QLabel, 
                            QHBoxLayout, 
                            QMessageBox,
                            QGroupBox,
                            QVBoxLayout,
                            QRadioButton,
                            QGridLayout,
                            QStyle
                            )
from PyQt5.QtGui import QIcon


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

class EpsxeWindow(QWidget):
	'''
	https://medium.com/@wilfilho/pyqt5-o-fantastico-mundo-das-guis-62914b1b39c1
	https://medium.com/@wilfilho/conhecendo-o-coracao-e-as-arterias-do-pyqt5-22ba4187531
	'''
	def __init__(self, parent=None):
		super(EpsxeWindow, self).__init__()
		self.window_icon = os.path.abspath(os.path.join(dir_of_executable, 'imgs', 'epsxe.png')) 
		self.setWindowIcon(QIcon())
		self.setWindowTitle('Epsxe-Qt-Gui')
		#self.setStyleSheet("background-color: #CD853F;") # Setar cor de fundo verde.
		self.setGeometry(150, 150, 550, 450)

		self.set_buttons()	
		#self.initUI()
		self.text = ''
		self.title_info = ''

	def set_buttons(self):
		# Botões com caixa de seleção		
		self.option_installer = QRadioButton("Instalar")
		self.option_installer.setChecked(True)
		self.option_download = QRadioButton("Baixar")
		self.option_configure = QRadioButton("Configurar")
		self.option_uninstall = QRadioButton("Desinstalar")

		# Box para Widgets
		self.groupbox = QGroupBox("Selecione uma opção e clique em OK")

		# Layout para os botões de seleção.
		self.layout_options = QVBoxLayout()
		self.layout_options.addWidget(self.option_download)
		self.layout_options.addWidget(self.option_installer)
		self.layout_options.addWidget(self.option_configure)
		self.layout_options.addWidget(self.option_uninstall)
		self.groupbox.setLayout(self.layout_options) 

		# Botões de clique.
		self.button_ok = QPushButton('OK', self)
		self.button_ok.setFixedWidth(110)
		self.button_ok.setFixedHeight(25)
		self.button_ok.setStyleSheet("border: 1px solid black;") 
		self.button_ok.setStyleSheet('{background-color: #A3C1DA; border:  none}')
		self.button_ok.clicked.connect(self.run)
		self.buttonExit = QPushButton('Sair', self)
		self.buttonExit.setFixedWidth(110)
		self.buttonExit.setFixedHeight(25)
		self.buttonExit.clicked.connect(self.click_exit_button)

		# Layout para botões de clique.
		self.layout_widgets_click = QHBoxLayout()
		self.layout_widgets_click.addWidget(self.button_ok)
		self.layout_widgets_click.addWidget(self.buttonExit)

		# Main Layout
		self.layout_master = QVBoxLayout()
		self.layout_master.addWidget(self.groupbox)
		self.layout_master.addLayout(self.layout_widgets_click)
		self.setLayout(self.layout_master)	

		#QMainWindow().statusBar()

	def run(self):
		if self.option_download.isChecked():
			self.download_epsxe()
			return
		elif self.option_installer.isChecked():
			epsxe_config.teste()
			self.text = 'Ação para instalar o programa.'
			self.title_info = 'Instalar'
		elif self.option_configure.isChecked():
			self.text = 'Ação para configurar o epsxe'
			self.title_info = 'Configurar Epsxe'
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
		'''
		exit_msg = QMessageBox.question(
						self, 
						'MessageBox', 
						"Deseja sair?", 
						QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
						)

		if exit_msg == QMessageBox.Yes:
			print('QMessageBox.Yes: saindo')
			sys.exit()
		'''
		sys.exit()

root = QApplication(sys.argv)
app = EpsxeWindow()
app.show()
sys.exit(root.exec_())