import sys

from nsense.dataset import file_type_count

if __name__ == "__main__":
	data_dir = sys.argv[1]
	print(file_type_count(data_dir))
