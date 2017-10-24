import sys

import numpy

from nsense.dataset import preprocess_corpus, extract_brown_from_zip

if __name__ == "__main__":
	data_dir = sys.argv[1]
	output_file = sys.argv[2]
	corpus = extract_brown_from_zip(data_dir)
	corpus = preprocess_corpus(corpus)

	ngram = dict()
	for sentence in corpus:
		for word, next_word in zip(sentence[:-1], sentence[1:]):
			word_form, word_tag = word
			next_word_form, next_word_tag = next_word

			if word_tag in ngram:
				ngram[word_tag][next_word_tag] = ngram[word_tag][next_word_tag] + 1 if next_word_tag in ngram[
					word_tag] else 1
			else:
				ngram[word_tag] = {next_word_tag: 1}

	union_keys = sorted(list(ngram))
	unnormalized = [[prior_dict[posterior] if posterior in prior_dict else 0 for posterior in union_keys] for
					prior_dict in
					[ngram[prior] for prior in list(ngram)]]
	for i, row in enumerate(unnormalized):
		row_sum = numpy.sum(row)
		if row_sum == 0:
			row_sum = 1
		unnormalized[i] = numpy.divide(row, row_sum)
	normalized = unnormalized

	with open(output_file, 'w') as output:
		output.write(" ".join(str(union_keys)) + "\n")
		output.writelines([" ".join([str(val) for val in row]) + "\n" for row in normalized])
