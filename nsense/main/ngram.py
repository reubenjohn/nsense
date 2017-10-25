import sys

import numpy

from nsense.dataset import preprocess_corpus, extract_brown_from_zip

if __name__ == "__main__":
	data_dir = sys.argv[1]
	output_dir = sys.argv[2]
	corpus = extract_brown_from_zip(data_dir)
	corpus = preprocess_corpus(corpus)

	ngram = dict()
	emmissions = dict()
	for sentence in corpus:
		for word_form, tag in sentence:
			if tag in emmissions:
				emmissions[tag][word_form] = emmissions[tag][word_form] + 1 if word_form in emmissions[tag] else 1
			else:
				emmissions[tag] = {word_form: 1}
		for word, next_word in zip(sentence[:-1], sentence[1:]):
			word_form, word_tag = word
			next_word_form, next_word_tag = next_word

			if word_tag in ngram:
				ngram[word_tag][next_word_tag] = ngram[word_tag][next_word_tag] + 1 if next_word_tag in ngram[
					word_tag] else 1
			else:
				ngram[word_tag] = {next_word_tag: 1}

	union_tags = sorted(list(ngram))
	unnormalized = [[prior_dict[posterior] if posterior in prior_dict else 0 for posterior in union_tags] for
					prior_dict in
					[ngram[prior] for prior in list(ngram)]]
	for i, row in enumerate(unnormalized):
		row_sum = numpy.sum(row)
		if row_sum == 0:
			row_sum = 1
		unnormalized[i] = numpy.divide(row, row_sum)
	normalized = unnormalized

	union_forms = sorted(set().union(*[list(emmissions[tag]) for tag in emmissions]))

	for tag in emmissions:
		emmission = emmissions[tag]
		emmission_count = 0
		for form_key in emmission:
			emmission_count = emmission_count + emmission[form_key]
		for form_key in emmission:
			emmission[form_key] = emmission[form_key] / emmission_count

	with open(output_dir + "transition.txt", 'w') as output:
		output.write(" ".join(union_tags) + "\n")
		output.writelines([" ".join([str(val) for val in row]) + "\n" for row in normalized])

	with open(output_dir + "emmission.txt", 'w') as output:
		output.writelines(
			[tag + "\t" + " ".join(
				[word_form + " " + str(emmissions[tag][word_form]) for word_form in sorted(emmissions[tag])]) + "\n"
			 for tag in sorted(emmissions)]

		)