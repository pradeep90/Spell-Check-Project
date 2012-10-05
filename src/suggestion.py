import re

class Suggestion(object):
    """Suggestion for the Spell Checker Program.

    Represents a word or phrase or sentence.
    It can be either a query sentence (with mistakes) or a suggestion
    generated by the program.
    """
    
    def __init__(self, term_list = None, suggestion_str = None, 
                 suggestion_type = 'phrase'):
        """

        Remember that the default suggestion_type is 'phrase', so even
        a word given without the explicit suggestion_type will be
        considered a phrase.
        """
        print 'Inside __init__'
        self.suggestion_type = suggestion_type
        if suggestion_str is not None:
            # Suggestion string is given priority
            self.set_suggestion_str(suggestion_str)
        elif term_list is not None:
            self.set_term_list(term_list)
        else:
            self.set_term_list([])

    def __eq__(self, other):
        print '__eq__'
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        elif isinstance(other, list):
            return self.term_list == other
        elif isinstance(other, str):
            return self.suggestion_str == other
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def set_term_list(self, given_term_list):
        """Set term_list to given_term_list and update suggestion_str.
        
        Arguments:
        - `given_term_list`:
        """
        self.term_list = given_term_list
        if not self.term_list:
            self.suggestion_str = ''
            return

        if self.suggestion_type == 'phrase':
            self.suggestion_str = ' '.join(str(term) for term in self.term_list)
        elif self.suggestion_type == 'sentence':
            # Duplicate of get_sentence_suggestion_from_phrase_suggestion
            self.suggestion_str = ' '.join(str(term) 
                                           for term 
                                           in self.term_list).capitalize() + '.'
        else:
            self.suggestion_str = self.term_list[0]

    def set_suggestion_str(self, given_suggestion_str):
        """Set suggestion_str to given_suggestion_str and update term_list.
        
        Arguments:
        - `given_suggestion_str`:
        """
        self.suggestion_str = given_suggestion_str
        if self.suggestion_type == 'phrase':
            # Get the space or comma-separated words
            self.term_list = filter(None, re.split('[, ]', self.suggestion_str))
        elif self.suggestion_type == 'sentence':
            self.term_list = filter(None, re.split('[, ]', self.suggestion_str))
        else:
            self.term_list = [self.suggestion_str]