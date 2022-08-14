# -*- coding: utf-8 -*-

##
# Copyright (с) Ildar Bikmamatov 2022
# License: MIT
##

import io, os

from PIL import Image


class DataStream:
	
	def __init__(self):
		self.dataset_name = os.path.join("data", "dataset")
	
	
	def open(self, *args):
		
		"""
			Open dataset
		"""
		
		self.dataset_name = os.path.join(*args)
	
	
	def flush(self):
		
		"""
			Flush dataset
		"""
		
		pass
	
	
	def close(self):
		
		"""
			Close dataset
		"""
		
		self.flush()
	
	
	def get_dataset_path(self, file_name = ""):
		
		"""
			Returns dataset full path
		"""
		
		if file_name == "":
			return os.path.join(self.dataset_name)
		return os.path.join(self.dataset_name, file_name)
	
	
	def list_files(self, path="", recursive=True):
	
		"""
			Returns files in folder
		"""
	
		def read_dir(path, recursive=True):
			res = []
			items = os.listdir(path)
			for item in items:
				
				item_path = os.path.join(path, item)
				
				if item_path == "." or item_path == "..":
					continue
				
				if os.path.isdir(item_path):
					if recursive:
						res = res + read_dir(item_path, recursive)
				else:
					res.append(item_path)
				
			return res
		
		try:
			dir_name = self.get_dataset_path(path)
			
			items = read_dir( dir_name, recursive )
				
			def f(item):
				return item[len(dir_name + "/"):]
			
			items = list( map(f, items) )
		
		except Exception:
			items = []
		
		return items
	
	
	def list_dirs(self, path=""):
		
		"""
			Returns dirs in folder
		"""
		
		dir_name = self.get_dataset_path(path)
		
		try:
			items = os.listdir(dir_name)
		
		except Exception:
			items = []
			
		return items
		
	
	def save_bytes(self, file_name, data):
		
		"""
			Save bytes to file
		"""
		
		file_path = self.get_dataset_path(file_name)
		file_dir = os.path.dirname(file_path)
		
		if not os.path.isdir(file_dir):
			os.makedirs(file_dir)
		
		f = open(file_path, 'wb')
		f.write(data)
		f.close()
		
	
	def read_bytes(self, file_name):
		
		"""
			Load bytes from file
		"""
		
		file_path = self.get_dataset_path(file_name)
		
		f = open(file_path, 'rb')
		data = f.read()
		f.close()
		
		return data
	
		
	def save_file(self, file_name, data):
		
		"""
			Save file
		"""
		
		bytes = None
		
		if isinstance(data, Image.Image):
			tmp = io.BytesIO()
			data.save(tmp, format='PNG')
			bytes = tmp.getvalue()
		
		if (isinstance(data, str)):
			bytes = data.encode("utf-8")
		
		if bytes is not None:
			self.save_bytes(file_name, bytes)
		
		pass
	
	
	
	def read_file(self, file_name):
		
		"""
			Read file
		"""
		
		return self.read_bytes(file_name)
	
	