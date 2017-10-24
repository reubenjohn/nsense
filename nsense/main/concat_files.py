import sys

from nsense.dataset import concat_files

if __name__ == "__main__":
	data_dir = sys.argv[1]
	concat_files(data_dir)

