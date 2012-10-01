#!/usr/bin/python

# Program to correct spelling errors.

import edit_distance_calculator
import itertools
import lexicon
import phrase
import spell_checker
import utils

dummy_posterior = 1 / 3.0
dummy_posterior_fn = lambda suggestion, query: dummy_posterior
lexicon = lexicon.Lexicon()

def get_inputs(filename = '../data/words.input'):
    """Return list of input queries read from filename.
    """
    f = open(filename, 'r')
    query_list = [line.strip() for line in f]
    f.close()
    print query_list
    return query_list

def write_outputs(query_list,
                  suggestion_dict,
                  output_filename = '../data/words.output'):
    """Write query_list along with suggestion_dict to output_filename.
    """
    f = open(output_filename, 'w')
    for i in xrange(len(query_list)):
        suggestions_str = '\t'.join(
            '{0}\t{1}'.format(' '.join(term for term in suggestion), posterior)
            for suggestion, posterior in suggestion_dict[query_list[i]])
        line = '{0}\t{1}'.format(query_list[i], suggestions_str)
        print line
        f.write(line + '\n')

def test_queries(test_name, query_input_file, query_output_file):
    """Test checker for query inputs (from query_input_file).

    Write the output to query_output_file.
    
    Arguments:
    - `query_input_file`:
    - `query_output_file`:
    """
    query_list = get_inputs(query_input_file)
    checker = spell_checker.SpellChecker()
    checker.get_posterior_fn = dummy_posterior_fn
    
    checker.run_spell_check(query_list)
    write_outputs(query_list, checker.get_suggestion_dict(), 
                  query_output_file)

def get_output_from_file(filename):
    """Return output of spell check from filename.

    Output: [query_list, suggestion_dict]
    """
    f = open(filename, 'r')
    file_input = [line.strip().split('\t') for line in f]
    f.close()
    print file_input
    suggestion_dict = dict((line_elements[0], 
                            zip (line_elements[1::2], 
                                 map(float, line_elements[2::2])))
                            for line_elements in file_input)
    query_list = suggestion_dict.keys()
    print suggestion_dict
    print query_list
    return [query_list, suggestion_dict]

def get_human_suggestions(filename):
    """Return human_suggestion_dict read from filename."""
    f = open(filename, 'r')
    file_input = [line.strip().split('\t') for line in f]
    f.close()
    print file_input
    human_suggestion_dict = dict([(line_elements[0], line_elements[1:]) 
                                  for line_elements in file_input])
    return human_suggestion_dict


def calc_stats(test_label, results_file, human_suggestions_file, stats_file):
    """Calc stats and write to results_file.
    
    Arguments:
    - `query_list`:
    - `suggestion_dict`:
    """
    query_list, suggestion_dict = get_output_from_file(results_file)
    human_suggestion_dict = get_human_suggestions(human_suggestions_file)
    dummy_spell_checker = spell_checker.SpellChecker()

    args = [query_list, suggestion_dict, human_suggestion_dict]
    EP = utils.get_EP(*args)
    ER = utils.get_ER(*args) 
    EF1 = utils.get_HM(EP, ER)
    stats = [EP, ER, EF1]
    print stats

    f = open(stats_file, 'a')
    f.write(' '.join(map(str, stats)) + '\n')
    f.close()

if __name__ == '__main__':
    # test_labels = ['words', 'phrases', 'sentences']
    # for test_label in test_labels:
    #     test_queries(test_label, 
    #                  '../data/' + test_label +  '.input', 
    #                  '../data/' + test_label + '.output')

    # get_inputs()
    # write_outputs(query_list = ['yo', 'boyz'],
    #               suggestion_dict = {'yo': [(['foo'], 0.7), (['bar'], 0.3)], 
    #                                  'boyz': [(['bar'], 0.4), (['baz'], 0.6)]})

    print get_output_from_file('../data/words.output')
    print get_human_suggestions('../data/words.tsv')
    calc_stats('words', '../data/words.output', 
               '../data/words.tsv', '../data/words.stats')
    # get_output_from_file('../data/phrases.output')
    # get_output_from_file('../data/sentences.output')

    

