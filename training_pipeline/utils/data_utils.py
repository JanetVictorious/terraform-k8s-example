import numpy as np

from training_pipeline.constants import DTYPES, CIDX, TARG_FEAT, MISSING_VAL


def read_csv(data_path: str) -> tuple[np.ndarray, dict]:
    """Read csv data file.
    """
    # Read file
    raw_data = []
    with open(data_path, 'r') as file:
        idx = 0
        for line in file:
            if idx == 0:
                idx += 1
                continue
            line = line.strip().split(',')
            for cidx in CIDX:
                if DTYPES[cidx] == 'int':
                    if line[cidx] in MISSING_VAL:
                        line[cidx] = None
                    # line[cidx] = int(line[cidx])
                    else:
                        line[cidx] = str(line[cidx])
                elif DTYPES[cidx] == 'float':
                    if line[cidx] in MISSING_VAL:
                        line[cidx] = np.nan
                    else:
                        line[cidx] = float(line[cidx])
                else:
                    if line[cidx] in MISSING_VAL:
                        line[cidx] = None
                    else:
                        line[cidx] = str(line[cidx])
            raw_data.append(line)

    # Store data as ndarray
    data = np.array(raw_data).astype('object')
    for cidx in CIDX:
        if DTYPES[cidx] == 'int':
            data[:, cidx] = data[:, cidx].astype('object')
        else:
            data[:, cidx] = data[:, cidx].astype(DTYPES[cidx])

    # In case target is str, convert to int
    targ_conv = {}
    if DTYPES[TARG_FEAT[0]] == 'object':
        k = 0
        for i in set([i[0] for i in data[:, TARG_FEAT] if i[0]]):
            if i in MISSING_VAL:
                continue
            targ_conv[i] = k
            k += 1
    return data, targ_conv
