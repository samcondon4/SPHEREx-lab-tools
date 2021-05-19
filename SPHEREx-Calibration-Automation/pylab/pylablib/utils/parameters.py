import pdb
import os
import pprint
from configparser import ConfigParser
import logging
#import astropy.cosmology as ac

"""
Functions to read/write parameters from/to .ini files using ConfigParser
"""

def get_params_dict(param_file_path):
    config = ConfigParser()
    config.read(param_file_path)

    dict_out = {}
    for section in config.sections():
        dict_sect = {}
        for (each_key, each_val) in config.items(section):
            dict_sect[each_key] = each_val

        dict_out[section] = dict_sect

    return dict_out

def write_config_file(params_out, config_filename_out):
    config_out = ConfigParser()

    for ikey, idict in params_out.items():
        if not config_out.has_section(ikey):

            config_out.add_section(ikey)
            for isect, ivals in idict.items():
                #pdb.set_trace()
                #print(ikey, isect, ivals)
                config_out.set(ikey, isect, str(ivals))

    #pdb.set_trace()
    # Write config_filename_out (check if overwriting externally)
    with open(config_filename_out, 'w') as conf:
        config_out.write(conf)

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def string_is_true(sraw):
    """Is string true? Returns boolean value.
    """
    s       = sraw.lower() # Make case-insensitive

    # Lists of acceptable 'True' and 'False' strings
    true_strings    = ['true', 't', 'yes', 'y', '1']
    false_strings    = ['false', 'f', 'no', 'n', '0']
    if s in true_strings:
        return True
    elif s in false_strings:
        return False
    else:
        logging.warning("Input not recognized for parameter: %s" % (key))
        logging.warning("You provided: %s" % (sraw))
        raise

def is_true(raw_params, key):
    """Is raw_params[key] true? Returns boolean value.
    """
    sraw    = raw_params[key]
    s       = sraw.lower() # Make case-insensitive

    # Lists of acceptable 'True' and 'False' strings
    true_strings    = ['True','true', 't', 'yes', 'y', '1']
    false_strings    = ['False','false', 'f', 'no', 'n', '0']
    if s in true_strings:
        return True
    elif s in false_strings:
        return False
    else:
        logging.warning("Input not recognized for parameter: %s" % (key))
        logging.warning("You provided: %s" % (sraw))
        raise

### FOR TESTING ###
if __name__=='__main__':
    import os, sys
    import pprint

    param_fp = sys.argv[1]
    print("")
    print("Testing %s on %s..." % (os.path.basename(__file__), param_fp))
    print("")
    pprint.pprint(get_params(param_fp))
