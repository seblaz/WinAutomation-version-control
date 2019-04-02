from win_auto import WinAutoCommand, WinAutoFolderStructure, SysFolder, Api
import os, shutil, subprocess
from xml.etree.ElementTree import fromstring

# WinAutoCommand('/ListRunning').run()

# xml = WinAutoCommand('/getallfolders', 'console').run()
# # print(xml)
# # print(str(xml).replace('\\r\\n', ''))
# # print('lala')

# sys_root_folder = SysProcessFolder(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'processes'))
# sys_root_folder.clear()

# structure = WinAutoFolderStructure(xml, sys_root_folder)
# # print(structure.root.Folders.Folder.Folders.children)
# structure.create_folder_structure()
# structure.export_processes()
# WinAutoStructure(str(xml))

# def run_command_and_parse_xml(args):
#     args = ['c:\Program Files\WinAutomation\WinAutomationController.exe'] + args     
#     xml = subprocess.check_output(args)
#     return xml

# winauto_processes_folders = run_command_and_parse_xml(['/getallfolders', 'console'])
# print(winauto_processes_folders)

# Api()._make_backup()
Api().import_()