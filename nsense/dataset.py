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


def extract_brown_from_zip(path):
	with ZipFile(path) as mzip:
		with mzip.open('brown/cats.txt') as cats_f:
			category_files = [mapping.decode('utf-8').split(' ')[0] for mapping in cats_f]
			for file_path in category_files:
				with mzip.open('brown/' + file_path) as zip_f:
					yield Object(path=file_path,
								 sentences=[[word.rsplit('/', 1) for word in line.decode('utf-8').split(' ')] for line
											in
											lines(zip_f)]
								 )


def detect_anomaly(sentence: iter):
	valid_count = 0
	pre_garbage_count = 0
	post_garbage_count = 0
	for word in sentence:
		if len(word) == 2:
			if post_garbage_count == 0:
				valid_count = valid_count + 1
			else:
				return True
		else:
			if valid_count == 0:
				pre_garbage_count = pre_garbage_count + 1
			else:
				post_garbage_count = post_garbage_count + 1
	if valid_count == 0:
		return True
	return pre_garbage_count, pre_garbage_count + valid_count


def preprocess_corpus(corpus):
	for file in corpus:
		for sentence in file.sentences:
			anomaly = detect_anomaly(sentence)
			if anomaly is True:
				print('Found anomalous sentence: ', sentence)
				continue

			pre_garbage_index, post_garbage_index = anomaly
			processed = sentence[pre_garbage_index:post_garbage_index]

			start_word = processed[0]
			end_word = processed[-1]
			if start_word[0].startswith("\t"):
				start_word[0] = start_word[0][1:]
			if end_word[0].endswith("\n"):
				end_word[0] = end_word[0][:-1]

			processed = [
				["\t", "\t"],
				*sentence[pre_garbage_index:post_garbage_index],
				["\n", "\n"]
			]
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
