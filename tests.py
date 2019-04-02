import os
import shutil
import tempfile
import unittest

from win_auto import *

class TestSysFolder(unittest.TestCase):
	def setUp(self):
		"""Creates a temporary directory before every test."""
		self.test_dir = tempfile.mkdtemp()
	
	def tearDown(self):
		"""Removes the directory after the test"""
		shutil.rmtree(self.test_dir)
	
	def test_create_when_the_folder_doesnt_exist_creates_it(self):
		path = os.path.join(self.test_dir, 'some_folder')
		assert(not os.path.exists(path))
		SysFolder(path).create()
		self.assertTrue(os.path.exists(path))

	def test_create_when_the_folder_exist_raises_FileExistsError(self):
		path = os.path.join(self.test_dir, 'some_folder')
		os.makedirs(path)
		assert(os.path.exists(path))
		with self.assertRaises(FileExistsError):
			SysFolder(path).create()

	def test_create_folder_when_the_folder_doesnt_exist_creates_it(self):
		SysFolder(self.test_dir).create_folder('some_folder')
		new_path = os.path.join(self.test_dir, 'some_folder')
		self.assertTrue(os.path.exists(new_path))

	def test_create_folder_when_the_folder_exists_does_nothing(self):
		path = os.path.join(self.test_dir, 'some_folder')
		os.makedirs(path)
		SysFolder(self.test_dir).create_folder('some_folder')
		self.assertTrue(os.path.exists(path))

	def test_clear_clears_files(self):
		file_ = os.path.join(self.test_dir, 'file.txt')
		open(file_, 'w').close()
		SysFolder(self.test_dir).clear()
		self.assertFalse(os.path.exists(file_))

	def test_clear_clears_folders(self):
		path = os.path.join(self.test_dir, 'some_folder')
		os.makedirs(path)
		SysFolder(self.test_dir).clear()
		self.assertFalse(os.path.exists(path))



if __name__ == '__main__':
    unittest.main()