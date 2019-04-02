import os
import shutil
import subprocess
import time
from random import randint

from untangle import parse


class WinAutomation(object):
	"""Provides methods to interact with WinAutomation."""
	ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
	BACKUP_DIR = os.path.join(ROOT_DIR, 'backups')
	WINAUTO_PATH = os.path.expanduser(os.path.join(
		'~', 'Documents', 'WinAutomation', 'Processes.dat'))
	BASIC_WINAUTO_PATH = os.path.join(ROOT_DIR, 'Processes.dat')
	PROCESSES_DIR = os.path.join(ROOT_DIR, 'processes')

	def export(self):
		"""Export all the processes in your WinAutomation console and
		delete all previous files in \processes.
		"""
		sys_root_folder = SysFolder(self.PROCESSES_DIR)
		sys_root_folder.clear()

		xml = WinAutoCommand('/getallfolders', 'console').run()
		structure = WinAutoFolderStructure(xml, sys_root_folder)
		structure.create_folder_structure()
		structure.export_processes()

	def import_(self):
		"""Delete all the processes in your console and replace them
		with the ones in the \processes folder. Side effect: this will
		also delete the triggers, schedules and logs on your console.
		"""
		self._make_backup()
		shutil.copyfile(self.BASIC_WINAUTO_PATH, self.WINAUTO_PATH)
		SysProcessesFolder(self.PROCESSES_DIR).import_()

	def restore(self, backup):
		"""This restores the backup specified in backup path."""
		if not os.path.isfile(backup):
			raise ValueError('The backup does not exist!')
		os.remove(self.WINAUTO_PATH)
		shutil.copyfile(backup, self.WINAUTO_PATH)

	def _make_backup(self):
		"""Makes a backup of the current WinAutomation 'Processes.dat'
		file in the 'self.BACKUP_DIR' directory.
		"""
		timestr = time.strftime("%Y-%m-%d %H%M%S")
		if not os.path.isdir(self.BACKUP_DIR):
			os.makedirs(self.BACKUP_DIR)
		backup_path = os.path.join(self.BACKUP_DIR, '{}{} {}'.format(
			timestr, randint(0, 9), 'Processes.dat'))
		shutil.move(self.WINAUTO_PATH, backup_path)


class SysFolder(object):
	"""Models a System Folder."""

	def __init__(self, path):
		"""path: folder path."""
		self.path = path

	def clear(self):
		"""Clears the folder of any content (both files and folders).
		"""
		if os.path.exists(self.path):
			shutil.rmtree(self.path)
		os.makedirs(self.path)

	def create(self):
		"""Creates the folder."""
		os.makedirs(self.path)

	def create_folder(self, folder):
		"""Creates the 'folder' inside this folder if it doesn't exist.
		"""
		folder_path = os.path.join(self.path, folder)
		if not os.path.isdir(folder_path):
			os.makedirs(folder_path)
		return SysFolder(folder_path)


class WinAutoCommand(object):
	"""Models a WinAutomation command."""
	CONTROLLER = r'c:\Program Files\WinAutomation\WinAutomationController.exe'

	def __init__(self, *args):
		"""args: any arguments that will be passed to the command."""
		self.args = args

	def run(self):
		"""Executes the command and returns the output."""
		return subprocess.check_output([self.CONTROLLER] + list(self.args)).decode("utf-8")


class WinAutoProcess(object):
	"""Models a WinAutomation process."""

	def __init__(self, path: str, name: str):
		"""path: process path without extension and including name.
		name: process name.
		"""
		self.path = path
		self.name = name

	def export(self, sys_process_folder: SysFolder):
		"""Exports the process to the sys_process_folder (string)."""
		export_file_path = '{}.waj'.format(
			os.path.join(sys_process_folder.path, self.name))
		WinAutoCommand('/export', self.path, export_file_path).run()
		print(self.path)


class WinAutoProcessesStructure(object):
	"""Models the structure of processes inside one of WinAutomation's
	folder.
	"""

	def __init__(self, xml):
		"""xml: list of WinAutomation's processes in xml format. This
		is usually the output of the
		'WinAutomationController /getprocessesoffolder' command.
		"""
		self.processes = parse(xml).Processes

	def export(self, sys_process_folder: SysFolder):
		"""Exports all WinAutomation's processes in 'self.processes' to
		'sys_process_folder'.
		"""
		for process in self.processes.children:
			WinAutoProcess(process.Path.cdata, process.Name.cdata).export(
				sys_process_folder)


class WinAutoFolderStructure(object):
	"""Models WinAutomation's folder structure in the system."""

	def __init__(self, xml: str, sys_root: SysFolder):
		"""xml: tree of WinAutomation's folder structure in xml format.
		This is usually the output of the 'WinAutomationController
		/getallfolders' command.
		sys_root: the folder where WinAutomation's structure will be
		recreated.
		"""
		self.winauto_root = parse(xml)
		self.sys_root = sys_root
		self._reset_structure()

	def _reset_structure(self):
		"""Resets the value of the variables 'self.current_winauto_folder'
		and 'self.current_sys_folder' used to export the processes from
		WinAutomation to the system.
		"""
		self.current_winauto_folder = self.winauto_root
		self.current_sys_folder = self.sys_root

	def _iterate(self, call=lambda x: None):
		"""Creates the structure in the system and calls the function
		'call' in every folder of the structure recursively. This
		function must receive the structure (self) as a parameter which
		provides the variables 'self.current_winauto_folder' and
		'self.current_sys_folder'.
		"""
		current_sys_folder = self.current_sys_folder
		for winauto_folder in self.current_winauto_folder.Folders.children:
			self.current_sys_folder = current_sys_folder.create_folder(
				winauto_folder.Name.cdata)
			self.current_winauto_folder = winauto_folder
			call(self)
			self._iterate(call)

	def create_folder_structure(self):
		"""Creates the folder structure in the system."""
		self._iterate()
		self._reset_structure()

	def export_processes(self):
		"""Exports all WinAutomation's processes to the system in
		'self.sys_root'.
		"""
		def _export_processes(structure):
			WinAutoProcessesStructure(
				WinAutoCommand(
					'/getprocessesoffolder',
					structure.current_winauto_folder.Path.cdata, 'console'
				).run()
			).export(structure.current_sys_folder)

		self._iterate(_export_processes)
		self._reset_structure()


class SysProcessesFolder(SysFolder):
	"""Models the root folder where the processes are stored in the
	system.
	"""

	def __init__(self, path):
		super().__init__(path)
		# self.current_winauto_path = ''

	def import_(self):
		for folder, subs, files in os.walk(self.path):
			winauto_dir = folder[len(self.path):].replace(os.sep, '/')
			for file in files:
				file_path = os.path.join(folder, file)
				winauto_process_path = '{}/{}'.format(winauto_dir, file)[:-4]
				WinAutoCommand('/import', file_path, winauto_process_path).run()
				print(winauto_process_path)
