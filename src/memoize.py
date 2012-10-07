# Adapted from http://blog.sujeet.me/2012/03/memoization-made-easy.html#more

# SPK:
# Main change: Wasn't able to pickle the dict when the function object
# itself was used as a key in _mem_tbls_ (cos of the scope or
# something being different when it was being dumped as compared to
# when it was being used as a key).
# Therefore, using the function name as a key.

import pickle

_mem_tbls_ = {}

memoize_table_file_name = 'memoize-table.dat'

def memoize(function):
    global _mem_tbls_
    init_memoize_table()

    print 'inside memoize'
    if function.__name__ not in _mem_tbls_:
        print 'Creating a new dict in memoize'
        _mem_tbls_ [function.__name__] = {}
    def memoized_function (*args):
        print 'args: ', args
        func_mem_tbl = _mem_tbls_ [function.__name__]
        if args not in func_mem_tbl:
            func_mem_tbl [args] = function (*args)
        else:
            print 'Hit in memoize table'
        return func_mem_tbl [args]
    return memoized_function

def init_memoize_table():
    """Load the memoize table (if it hasn't already been loaded) from a file.
    """
    global _mem_tbls_
    if _mem_tbls_:
        # The table has already been read cos of some other memoized
        # function.
        return

    try:
        with open(memoize_table_file_name, 'rb') as f:
            _mem_tbls_ = pickle.load(f)
            f.close()
            print 'Memoize Table loaded from file.'
    except IOError:
        print 'Memoize file does not exist'
    # print '_mem_tbls_', _mem_tbls_

def save_memoize_table():
    """Load the memoize table (if it exists) from a file.
    """
    global _mem_tbls_
    f = open(memoize_table_file_name, 'wb')
    pickle.dump(_mem_tbls_, f)
    f.close()
    print 'Memoize Table saved to file.'

