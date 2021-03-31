import pdb
import os
import pprint
from configparser import ConfigParser
import logging
#import astropy.cosmology as ac

def get_params(param_file_path):
    """
    Get parameter values and return them in the form of a dictionary.

    Parameters
    ----------
    param_file_path : str
        path to parameter file

    Returns
    -------
    params : dict
    """

    config = ConfigParser()
    config.read(param_file_path)

    params = get_params_dict(config)

    logging.info("---------- PARAMETER VALUES ----------")
    logging.info("======================================")
    logging.info("\n" + pprint.pformat(params, indent=4) + "\n")

    #write_config_file(params, param_file_path)
    #pdb.set_trace()
    return params

def get_params_dict(config_in):
    dict_out = {}
    for section in config_in.sections():
        dict_sect = {}
        for (each_key, each_val) in config_in.items(section):
            #print(each_key)
            #print(each_val)
            dict_sect[each_key] = each_val

        dict_out[section] = dict_sect

    return dict_out

def write_config_file(params_out, config_filename_out):
    config_out = ConfigParser()
    #pdb.set_trace()
    for ikey, idict in params_out.items():
        #pdb.set_trace()
        if not config_out.has_section(ikey):
            config_out.add_section(ikey)
            #pdb.set_trace()
            for isect, ivals in idict.items():
                #pdb.set_trace()
                config_out.set(ikey, isect, ivals)


    #pdb.set_trace()
    #config_filename_out = "..\\pylab\\pylabcal\\config\\setup_test_write.cfg"
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

### FOR TESTING ###
if __name__=='__main__':
    import os, sys
    import pprint

    param_fp = sys.argv[1]
    print("")
    print("Testing %s on %s..." % (os.path.basename(__file__), param_fp))
    print("")
    pprint.pprint(get_params(param_fp))
