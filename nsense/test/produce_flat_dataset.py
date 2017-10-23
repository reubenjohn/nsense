import sys

from nsense.dataset import flatten_data_source

if __name__ == "__main__":
	data_dir = sys.argv[1]
	flat_dir = sys.argv[2]
	flatten_data_source(data_dir, flat_dir)