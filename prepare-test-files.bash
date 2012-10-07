#!/bin/bash
# Prepare test input and expected output files
# Args:
# $1 - Number of lines of input to take from the original input files
if [ $# -eq 1 ]; then
    N=$1
else
    N=5
fi

data_folder=data
dataset_name=trec

for test_label in words phrases sentences; do
    echo $test_label

    dataset_folder=$dataset_name-$test_label
    original_test_file=$data_folder/$dataset_folder/$test_label.tsv
    input_file=$data_folder/$test_label.input
    output_test_file=$data_folder/$test_label.tsv

    echo head ${original_test_file} -n $N \| cut -f 1 \> ${input_file}
    echo head ${original_test_file} -n $N \> ${output_test_file}
done

