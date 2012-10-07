#!/usr/bin/python

# Program to correct spelling errors.

from datetime import datetime
import edit_distance_calculator
import itertools
import lexicon
import math
from memoize import save_memoize_table
from suggestion import Suggestion
import phrase
import spell_checker
import sys
import utils

dummy_posterior = 1 / 3.0
dummy_prior = 1 / 3.0
dummy_posterior_fn = lambda suggestion, query: math.exp(math.log(dummy_prior) + phrase.get_likelihood(query, suggestion))
lexicon = lexicon.Lexicon()

def get_inputs(test_label, filename = '../data/words.input'):
    """Return list of input queries read from filename.

    Lowercase all the words.
    If a query is a sentence, remove the period at the end.
    """
    f = open(filename, 'r')
    query_list = [Suggestion(suggestion_str = line.strip(), 
                             suggestion_type = test_label[:-1]) 
                             for line in f]
    f.close()
    # if test_label == 'sentences':
    #     query_list = [utils.get_phrase_from_sentence(query) 
    #                   for query in query_list]

    # query_list = [query.lower() for query in query_list]
    
    print 'query_list', query_list
    return query_list

def write_outputs(test_label, 
                  query_list,
                  suggestion_dict,
                  output_filename = '../data/words.output'):
    """Write query_list along with suggestion_dict to output_filename.
    """
    f = open(output_filename, 'w')

    # if test_label == 'sentences':
    #     # Capitalize each sentence and add a period at the end.
    #     suggestion_dict = dict([
    #         (utils.get_sentence_from_phrase(query), 
    #          [(suggestion.set_suggestion_type('sentence'), 
    #            posterior) 
    #           for suggestion, posterior in suggestion_list])
    #          for query, suggestion_list in suggestion_dict.iteritems()])

    for i in xrange(len(query_list)):
        suggestions_str = '\t'.join(
            '{0}\t{1}'.format(str(suggestion),
                # ' '.join(term for term in suggestion), 
                              posterior)
            for suggestion, posterior in suggestion_dict[query_list[i]])
        line = '{0}\t{1}'.format(str(query_list[i]), suggestions_str)
        print 'line:', line.replace('\t', '\n')
        f.write(line + '\n')

def test_queries(test_label, query_input_file, query_output_file):
    """Test checker for query inputs (from query_input_file).

    Write the output to query_output_file.
    For sentences, capitalize the first word and add a period at the
    end to the suggestions.

    Arguments:
    - `test_label`:
    - `query_input_file`:
    - `query_output_file`:
    """
    query_list = get_inputs(test_label, query_input_file)
    checker = spell_checker.SpellChecker()

    if sys.argv[1] == 'dummy-test':
        checker.get_posterior_fn = dummy_posterior_fn
    
    checker.run_spell_check(query_list)
    suggestion_dict = checker.get_suggestion_dict()

    print 'suggestion_dict', suggestion_dict
    
    # TODO: Remove this
    save_memoize_table()
    write_outputs(test_label, suggestion_dict.keys(), suggestion_dict, 
                  query_output_file)

def get_output_from_file(test_label, filename):
    """Return output of spell check from filename.

    The file contains query TAB suggestion1 TAB posterior1 TAB ...
    Output: [query_list, suggestion_dict]
    """
    f = open(filename, 'r')
    file_input = [line.strip().split('\t') for line in f]
    f.close()
    print 'file_input', file_input
    suggestion_dict = dict((Suggestion(suggestion_str = line_elements[0], 
                                       suggestion_type = test_label[:-1]), 
                            zip ([Suggestion(suggestion_str = suggestion_str, 
                                             suggestion_type = test_label[:-1]) 
                                             for suggestion_str in line_elements], 
                                 map(float, line_elements[2::2])))
                            for line_elements in file_input)
    query_list = suggestion_dict.keys()
    print 'suggestion_dict', suggestion_dict
    print 'query_list', query_list
    return [query_list, suggestion_dict]

def get_human_suggestions(test_label, filename):
    """Return human_suggestion_dict read from filename.

    Each of the sentences is like 'Yo boyz i am sing song.' with the
    capitalization and period preserved.
    """
    f = open(filename, 'r')
    file_input = [line.strip().split('\t') for line in f]
    f.close()
    print 'file_input', file_input
    human_suggestion_dict = dict([(line_elements[0], 
                                   line_elements[1:]) 
                                  for line_elements in file_input])
    return human_suggestion_dict


def calc_stats(test_label, results_file, human_suggestions_file, stats_file):
    """Calc stats and write to results_file.
    
    Arguments:
    - `query_list`:
    - `suggestion_dict`:
    """
    query_list, suggestion_dict = get_output_from_file(test_label, results_file)

    human_suggestion_dict = get_human_suggestions(test_label, human_suggestions_file)
    dummy_spell_checker = spell_checker.SpellChecker()

    args = [query_list, suggestion_dict, human_suggestion_dict]
    EP = utils.get_EP(*args)
    ER = utils.get_ER(*args) 
    EF1 = utils.get_HM(EP, ER)
    stats = [EP, ER, EF1]
    print 'stats', stats

    f = open(stats_file, 'a')
    stats_str = 'Timestamp: {0}\tLabel: {1}\tEP: {2}\tER: {3}\tEF1: {4}\n'.format(
        str(datetime.now()), test_label, *stats)
    print 'stats_str', stats_str
    f.write(stats_str)
    f.close()

if __name__ == '__main__':
    commandline_args_str = 'Format: ' + sys.argv[0] + ' arg\n' + 'arg = run-test: run all tests and write to results file.\n' + 'arg = calc-stats: calculate stats from results in file.\n'

    # test_labels = ['phrases']
    test_labels = ['words', 'phrases', 'sentences']
    if len (sys.argv) != 2:
        print 'commandline_args_str', commandline_args_str
        exit (0)
    elif sys.argv[1] in ['run-test', 'dummy-test']:
        for test_label in test_labels:
            test_queries(test_label, 
                         '../data/' + test_label +  '.input', 
                         '../data/' + test_label + '.output')
        save_memoize_table()
    elif sys.argv[1] == 'calc-stats':
        for test_label in test_labels:
            calc_stats(test_label, 
                       '../data/' + test_label + '.output', 
                       '../data/' + test_label + '.tsv', 
                       '../data/' + test_label + '.stats')
        save_memoize_table()
    else:
        print 'commandline_args_str', commandline_args_str
        exit (0)
