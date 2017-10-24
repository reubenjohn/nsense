import os
from shutil import copyfile
from zipfile import ZipFile


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


def add_words_to_dict(word_dict, file):
	for index, line in enumerate(file):
		if index % 100000 == 0:
			print(index)
		if index == 1000000:
			return
		for word in line.split():
			if word in word_dict:
				word_dict[word] = word_dict[word] + 1
			else:
				word_dict[word] = 1


def lines(file):
	while True:
		chars = file.readline()
		if len(chars) == 0:
			return
		if chars != b'\n':
			yield chars


Object = lambda **kwargs: type("Object", (), kwargs)


def extract_corpus_from_zip(path):
	with ZipFile(path) as mzip:
		files = mzip.namelist()[1:]
		for file_path in files:
			with mzip.open(file_path) as zip_f:
				yield Object(path=file_path,
							 sentences=[[word.split('/') for word in line.decode('utf-8').split(' ')] for line in
										lines(zip_f)]
							 )


def preprocess_corpus(corpus):
	for file in corpus:
		for sentence in file.sentences:
			start = 0
			for word in sentence:
				if len(word) != 2:
					start = start + 1
			if start == len(sentence):
				continue
			sentence = sentence[start:]
			processed = [["\t", "\t"],
						 [sentence[0][0][1:], sentence[0][1]] if sentence[0][0][0] == "\t" else sentence[0],
						 *sentence[1:-1],
						 ([sentence[-1][0], sentence[-1][1][:-1]]
						  if sentence[-1][1][-1] == "\n"
						  else sentence[-1]) if len(sentence[-1]) >= 2 else None
						 ]
			if processed[-1] is None:
				processed[-1] = ["\n", "\n"]
			else:
				processed.append(["\n", "\n"])
			yield processed


def word_count(path):
	words = dict()
	for p in os.walk(path):
		files = p[2]
		for file in files:
			with open(p[0] + '/' + file, 'r') as f:
				add_words_to_dict(words, f)
	return words


def concat_files(path):
	with open(path + '/../compiled.txt', 'w') as out:
		for p in os.walk(path):
			files = p[2]
			for file_i, file in enumerate(files):
				print(file_i, ' ', end='')
				out.write('`')
				try:
					with open(p[0] + '/' + file, 'r') as f:
						out.writelines(f)
				except Exception as e:
					print(e)
		out.write('`')
		print('Compiled')
