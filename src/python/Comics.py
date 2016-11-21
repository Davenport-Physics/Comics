#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Comics.py
#  
#  Copyright 2014-2016 Michael Davenport <Davenport.physics@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os

Verbose = False
ProgramVersion = .30

"""

main function initializes a Comics object, and then calls the run_loop
function passing the Comics object by reference.

The run_loop function handles input from the user, and allows the user
to run specific commands from the shell that is provided.

"""
def main():
	
	global ProgramVersion
	
	print("Comics version %lf" % (ProgramVersion))
	
	
	obj = Comics()
	print("Please start by typing the command folder")
	run_loop(obj)

	return 0

"""

run_loop is passed a Comics object, and the user is asked to give input.

The commands that are recognized by the script are.

"folder", which allows the user to specify the directory the program should
look at.

"init", reads the init file. This allows the user to edit the file during runtime
and reload it.

"auto", renames the files by the data specified in the list.txt document
or one that is equivalent.

"print", prints out all the filenames in the directory specified by the user.

"quit/exit", halts execution of the program.

"""
def run_loop(obj):
	
	global Verbose
	
	while True:
		
		#quits ctrl+d gracefully
		try:
			command = str(input("> "))
		except EOFError:
			print("\n")
			break
		
		if command in "folder":
			
			directory = str(input("Please type in directory verbatim > "))	
			obj.set_directory( directory )
			
		elif command in "init":
			
			obj.read_init_file()
			
		elif "remove" in command:
			
			temp = command.split()
			
			if len(temp) < 2:
				print("Not enough arguments")
			else:
				if obj.does_directory_exist() == True:
					remove(obj, temp[1])
				else:
					print("Please enter a valid directory")
				
		elif command in "auto":
			
			if obj.does_directory_exist() == True:
				rename_files(obj)
			else:
				print("Please enter a valid directory")
				
		elif command in "rauto":
			
			if obj.does_directory_exist() == True:
				obj.find_recursive_directories()
				rename_files(obj, True)
			else:
				print("Please enter a valid directory")
				
		elif command in "shorten":
			
			if obj.does_directory_exist() == True:
				shorten(obj)
			else:
				print("Please enter a valid directory")
				
		elif command in "database" or command in "db":
			
			if obj.does_directory_exist() == True:
				obj.find_recursive_directories()
				write_database(obj)
			
		elif command in "print":
			
			obj.print_names()
			
		elif command in "debug":
			
			Verbose = True
			
		elif command in "quit" or command in "exit":
			
			break
			
		elif command in "help" or command in "Help":
			
			print("folder - Changes current directory to specified folder")
			print("init   - Reads the config file. Great for making additions on the fly")
			print("print  - Prints out files within the current directory")
			print("quit   - Exits the program")
			print("debug  - Prints extra information")
			
		else:
			
			print("Incorrect command")
		

def remove(obj, subname):
	
	global Verbose
	
	directory = obj.get_directory()
	
	for File in os.listdir(directory):
		
		string = File
		string = string.replace(subname, "")
		os.rename(os.path.join(directory, File) , os.path.join(directory, string))
		

def shorten(obj):
	
	global Verbose
	
	directory = obj.get_directory()
	
	for File in os.listdir(directory):
		
		string = File
		temp = string.split()
		string = ""
		for i in range(len(temp)):
			if i+1 != len(temp):
				string += temp[i] + " "
			else:
				string += temp[i]
				
		if len(string) > 1:
			os.rename(os.path.join(directory, File) , os.path.join(directory, string))

"""

rename_files is passed a Comics Object, and renames each of the files in
the directory the user specified, by data found in list.txt or an equivalent
file.

"""
def rename_files(obj, Recursive = False):
	
	global Verbose
	
	if Recursive == False:
		directory = obj.get_directory()
		rename_algorithm(obj, directory)
	else:
		directories = obj.get_recursive_directories()
		depth = obj.get_recursive_depth()
		for i in range(depth, -1, -1):
			for x in range(len(directories[i])-1, -1, -1):
				try:
					rename_algorithm(obj, directories[i][x])
				except IndexError:
					print("Exception i = %d, x = %d" %(i,x))
		
	
	#Lists all the files within the directory the user provided.
	

			
def rename_algorithm(obj, directory):

	for File in os.listdir(directory):
		
		#rename variable is used to determine whether the file needs to be renamed.
		rename = False
		string = File
		
		"""
		
		Runs this algorithm twice.
		
		It checks to see if there is the character ';' in the current
		name. If there is, it splits up the string, and checks to see
		if the first substring is located within the File name. If it is,
		then it replaces that string with the second substring.
		
		If ';' is not in the name string, then it checks to see
		if name is within the file string. If it is, it replaces
		the name string within the file string, with an empty character ""
		
		"""
		for i in range(2):
			
			for name in obj.get_names():
			
				if ';' in name:
				
					temp = name.split(";")
				
					if temp[0] in string:
					
						string = string.replace(temp[0] , temp[1])
						rename = True
				
				elif name in string:
				
					string = string.replace(name , "")
					rename = True
				
		if rename:
			
			if Verbose == True:
			
				print(File + " renamed as " + string)
			
			try:
				os.rename(os.path.join(directory, File) , os.path.join(directory, string))
			except FileNotFoundError:
				if Verbose == True:
					print("Supressed bug, FileNotFoundError")
					
					
def write_database(obj):
	
	fp = open("Comics.db", "w")
	
	for i in obj.get_files():
		temp = i.replace(".cbr", "")
		temp = temp.replace(".CBR", "")
		temp = temp.replace(".cbz", "")
		temp = temp.replace(".CBZ", "")
		temp = temp.split()
		for y in range(len(temp)):
			if y+1 != len(temp):
				fp.write("%s\t" % (temp[y]))
			else:
				fp.write("%s" % (temp[y]))
		fp.write("\n")
	
	fp.close()

		
class Comics:
	
	def __init__(self,filename = "list.txt"):
		
		self.filename = filename
		self.read_init_file()
		self.Files = []
		self.DirectoryExists = False
		self.RecursiveDirectories = []
		self.RecursiveDepth = 0
		
	def read_init_file(self):

		self.names = []
		
		
		string	= ""
		fp		= open(self.filename, "r")
		
		for name in fp:
			
			string += name
			
		self.names = string.splitlines()
			
	def set_directory(self , directory):
		
		try:
			os.listdir(directory)
		except	FileNotFoundError:
			print("Directory %s does not exist. Please try again" % (directory))
			self.DirectoryExists = False
			return -1
		
		self.directory = directory
		self.DirectoryExists = True
		
	def find_recursive_directories(self):
		
		self.Files = []
		self.RecursiveDirectories = []
		self.RecursiveDirectories.append([])
		self.RecursiveDepth = 0
		
		if self.DirectoryExists == True:
			
			#First order directory
			for File in os.listdir(self.directory):
				self.check_directory(self.directory ,File)
				
			if len(self.RecursiveDirectories[0]) > 0:
				self.find_n_order_directories()
					
	#Private Function		
	def find_n_order_directories(self):
		
		while True:
			
			self.RecursiveDepth += 1
			self.RecursiveDirectories.append([])
			for i in range(len(self.RecursiveDirectories[self.RecursiveDepth-1])):
				for File in os.listdir(self.RecursiveDirectories[self.RecursiveDepth-1][i]):
					self.check_directory(self.RecursiveDirectories[self.RecursiveDepth-1][i], File)
				
			if len(self.RecursiveDirectories[self.RecursiveDepth]) == 0:
				self.RecursiveDepth -= 1
				break

	#Private Function
	def check_directory(self, directory, File):
		
		global Verbose
		
		temp = directory + "/" + File
		if os.path.isdir(temp) == True:
			if Verbose == True:
				print(File)
			self.RecursiveDirectories[self.RecursiveDepth].append(temp)
		else:
			self.Files.append(File)
			
	def get_recursive_directories(self):
		
		return self.RecursiveDirectories
		
	def get_recursive_depth(self):
		
		return self.RecursiveDepth
				
	def get_directory(self):
		
		return self.directory
		
	def does_directory_exist(self):
		
		return self.DirectoryExists
		
	def get_files(self):
		
		return self.Files
			
	def get_names(self):
		
		return self.names
		
	def print_names(self):
		
		for x in self.names:
			print(x)
			

if __name__ == '__main__':
	main()

