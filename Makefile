# Prepare test input and out files
ORIGINAL_TEST_FILE = data/trec-phrases/phrases.tsv
INPUT_FILE = data/phrases.input
OUTPUT_TEST_FILE = data/phrases.tsv
N = 1

prepare_test_files:
	head ${ORIGINAL_TEST_FILE} -n $N | cut -f 1 > ${INPUT_FILE}
	head ${ORIGINAL_TEST_FILE} -n $N > ${OUTPUT_TEST_FILE}
