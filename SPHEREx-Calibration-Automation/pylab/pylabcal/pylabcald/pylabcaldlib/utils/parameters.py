import pdb
import os
import pprint
from configparser import ConfigParser
import logging
import astropy.cosmology as ac

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

    # Get "raw" dictionaries from `config` object
    #pdb.set_trace()
    raw_params = dict(config.items('general'))
    raw_io_params = dict(config.items('io'))
    raw_io_params['param_file_path'] = os.path.abspath(param_file_path) # Store parameter file path
    #raw_storage_params = dict(config.items('storage'))
    raw_metadata_params = dict(config.items('metadata'))
    raw_cosmo_params = dict(config.items('cosmology'))
    raw_monochrometer_params = dict(config.items('monochrometer'))


    # Convert "raw" config dictionary to "organized" dictionary `params`
    params = {}
    params['general'] = get_general_params(raw_params)
    params['io'] = get_io_parameters(raw_io_params)
    #params['storage'] = get_storage_parameters(raw_io_params)
    params['metadata'] = get_metadata_parameters(raw_metadata_params)
    #params['cosmo'] = get_cosmology_parameters(raw_cosmo_params)
    params['monochrometer'] = get_monochrometer_parameters(raw_monochrometer_params)

    logging.info("---------- PARAMETER VALUES ----------")
    logging.info("======================================")
    logging.info("\n" + pprint.pformat(params, indent=4) + "\n")

    #pdb.set_trace()
    return params

def get_general_params(raw_params):
    params = {} # Initialize parameter dictionary
    params['automate']  = raw_params['automate']

    return params

def get_io_parameters(raw_params):
    io = {}

    io['temp_storage_folder']       = raw_params['temp_storage_folder']
    io['permanent_storage_folder']  = raw_params['permanent_storage_folder']
    io['compression_type']          = raw_params['compression_type']
    io['storage_type']              = raw_params['storage_type']
    io['keywords']              = raw_params['keywords']
    io['suffix']              = raw_params['suffix']

    return io

def get_metadata_parameters(raw_params):
    metadata = {}

    metadata['power_meter']     = raw_params['power_meter']
    metadata['filter_wheel_1']  = raw_params['filter_wheel_1']
    metadata['filter_wheel_2'] = raw_params['filter_wheel_2']
    metadata['encoder_1']       = raw_params['encoder_1']
    metadata['encoder_2']       = raw_params['encoder_2']
    metadata['cryo_temperature']= raw_params['cryo_temperature']

    return metadata

def get_cosmology_parameters(raw_params):
    '''
    Returns
    -------
    cosmo : astropy.cosmology object
        object containing cosmological parameters
    '''
    omega_m0    = float(raw_params['omega_m'])    # Present-day matter density
    omega_l0    = float(raw_params['omega_l'])    # Present-day dark energy density
    omega_k0    = float(raw_params['omega_k'])    # Present-day spatial curvature density
    hubble_h0   = float(raw_params['h'])          # Present-day reduced Hubble constant: h0 = H0 / (100 km/s/Mpc)

    H0          = hubble_h0*100.
    cosmo       = ac.LambdaCDM(H0=H0, Om0=omega_m0, Ode0=omega_l0)

    return cosmo

def get_monochrometer_parameters(raw_params):
    mono = {}

    mono['wavelength_start']    = raw_params['wavelength_start']
    mono['wavelength_stop']     = raw_params['wavelength_stop']
    mono['wavelength_step']     = raw_params['wavelength_step']

    return mono

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
