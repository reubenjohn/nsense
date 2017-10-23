import sys

from nsense.dataset import file_type_count, word_count

if __name__ == "__main__":
	data_dir = sys.argv[1]
	print(word_count(data_dir))
