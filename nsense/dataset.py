import os
from shutil import copyfile


def flatten_data_source(data_dir_path: str, output_flat_dir_path: str, file_patterns=['.c', '.h']):
	output_flat_dir_path = output_flat_dir_path + '/'
	for p in os.walk(data_dir_path):
		rel = p[0].lstrip(data_dir_path) + '/'
		flat_rel = rel.replace("/", "_")
		for file in p[2]:
			for pattern in file_patterns:
				if file.endswith(pattern):
					print('cp "%s" "%s"' % (p[0] + "/" + file, output_flat_dir_path + flat_rel + file))
					copyfile(p[0] + "/" + file, output_flat_dir_path + flat_rel + file)


def file_type_count(path):
	extensions = dict()
	file_count = 0
	for p in os.walk(path):
		files = p[2]
		file_count = file_count + len(files)
		for file in files:
			r_i = file.rfind(".")
			if r_i != -1:
				extension = file[r_i + 1:]
				if extension in extensions:
					extensions[extension] = extensions[extension] + 1
				else:
					extensions[extension] = 1
		print(file_count)
	return extensions


def word_count(path):
	words = dict()
	for p in os.walk(path):
		files = p[2]
		for file in files:
			try:
				with open(p[0] + '/' + file, 'r') as f:
					for line in f:
						for word in line.split():
							if word in words:
								words[word] = words[word] + 1
							else:
								words[word] = 1
			except Exception as e:
				print(e)
	return words
