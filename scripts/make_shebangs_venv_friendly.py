#!/usr/bin/env python

import os, re, shutil

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
directory_blacklist = ['.git', 'env']
directory_blacklist_set = set(directory_blacklist)

if __name__ == "__main__":
	for current_directory, subdirectories, files in os.walk(ROOT_DIR):
		#print("Checking {0}:{1}".format(current_directory, files))
		# Prune any blacklisted directories
		present_blacklisted_directories = directory_blacklist_set.intersection(subdirectories)
		for pbd in present_blacklisted_directories:
			subdirectories.remove(pbd)

		# Process the files in this current directory by checking the first line of the code for a normal, generic shebang (#!/usr/bin/python3) and replace it with a virtual environment friendly one
		for f in files:
			original_file_path = os.path.join(current_directory, f)
			new_file_path = original_file_path + "~"
			original_file = open(original_file_path, 'r')
			try:
        	                first_line = original_file.readline()
                	        if re.match('\#\!\/usr\/bin\/python3', first_line):
                        	        print("Updating:" + original_file_path)
                                	try:
	                                        new_file_path = original_file_path + "~"
        	                                new_file = open(new_file_path, 'w')
                	                        new_file.write("!#/usr/bin/env python3\n")
                        	                shutil.copyfileobj(original_file, new_file)
                                	        original_file.close()
                                        	new_file.close()
	                                        os.remove(original_file_path)
        	                                shutil.copy(new_file_path, original_file_path)
                	                finally:
                        	                new_file.close()
                                	        os.remove(new_file_path)
			finally:
				original_file.close()
