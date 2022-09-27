import numpy as np

# # Example csv
# # Target column
# TARGET = 'y'

# # Data specs
# CNAMES = ['y', 'x1', 'x2', 'x3']
# DTYPES = ['object', 'float', 'int', 'object']
# CIDX = [i for i in range(len(CNAMES))]

# Target column
TARGET = 'species'

# Data specs
CNAMES = ['species', 'island', 'culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex']
DTYPES = ['object', 'object', 'float', 'float', 'int', 'int', 'object']
CIDX = [i for i in range(len(CNAMES))]

TARG_FEAT = [i for i in CIDX if CNAMES[i] == TARGET]
NUM_FEAT = [i for i in CIDX if DTYPES[i] == 'float' and CNAMES[i] != TARGET]
CAT_FEAT = [i for i in CIDX if DTYPES[i] != 'float' and CNAMES[i] != TARGET]

# Missing value types
MISSING_VAL = ['', 'nan', 'NA', 'NaN', 'None', '.', np.nan, None, 'na']
