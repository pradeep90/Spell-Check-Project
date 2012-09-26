class SpellChecker(object):
    """Suggest corrections for errors in queries.
    """
    
    def __init__(self):
        """Nothing much.
        """
        print 'Yo, boyz!'

    def generate_suggestions(self, query):
        """Return suggestions for query along with their posterior probabilities.

        Return (Suggestions, Posteriors) where Suggestions is a list
        of suggestions and Posteriors is a list of the corresponding
        posterior probabilities.
        
        Arguments:
        - `query`:
        """
        suggestions = ["believe", "buoyant", "committed", "distract", 
                       "ecstacy", "fairy", "hello", "gracefully", 
                       "liaison", "occasion", "possible", "throughout", 
                       "volley", "tattoos", "respect"]

        posteriors = [0.69, 0.15, 0.93, 0.30, 0.30, 0.31, 0.15, 
                      0.38, 0.48, 0.62, 0.11, 0.22, 0.44, 0.30, 0.82]
        return (suggestions, posteriors)

if __name__ == '__main__':
    spell_checker = SpellChecker()
    print spell_checker.generate_suggestions('yo')
