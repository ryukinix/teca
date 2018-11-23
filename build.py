import os

""" O arquivo build.py faz a instalação da teca.spec no qual é 
importante para criação do instalador teca.exe
"""

os.system("pyinstaller teca.spec")
