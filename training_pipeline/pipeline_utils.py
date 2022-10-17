import os
import logging

from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import KBinsDiscretizer, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, confusion_matrix

import dill

from training_pipeline.constants import FILENAME, TARGET, TARG_FEAT, MISSING_VAL, NUM_FEAT, CAT_FEAT
from training_pipeline.utils.data_utils import read_csv
from training_pipeline.utils.models import ModelName, _services
from training_pipeline.utils.params import model_params


def run_pipeline(input_dir: str = ...,
                 output_dir: str = ...,
                 model_name: str = ...) -> None:
    """Train classifier.

    Given an input dataset, split, preprocess, train model, and export results.
    """
    logging.info('=' * 50)

    # Create model object
    logging.info(f'Creating model object {model_name}...')
    params = model_params.get(model_name)
    MODEL = _services.get(ModelName(model_name).value, **params)

    # Create output directory if not exists
    logging.info('Create output directory...')
    output_path = os.path.join(output_dir, 'serving')
    os.makedirs(output_path, exist_ok=True)

    logging.info(f'Target name: {TARGET}')

    # Load data
    data_path = os.path.abspath(os.path.join(input_dir, FILENAME))
    logging.info(f'Loading data from: {data_path}')

    data, targ_conv = read_csv(data_path)

    logging.info(f'Shape of data: {(data.shape)}')

    logging.info('Make sure target is present...')

    # Make sure target is present
    missing_targ = [i[0] not in MISSING_VAL for i in data[:, TARG_FEAT]]
    data = data[missing_targ, :]

    logging.info(f'Shape of dataframe: {data.shape}')

    # Columns for modeling features
    features = NUM_FEAT + CAT_FEAT
    logging.info(f'Nr of modeling features: {len(features)}')

    logging.info('Create preprocessors...')

    # Numerical preprocessor
    num_pp = make_pipeline(
        SimpleImputer(strategy='median'),
        KBinsDiscretizer(n_bins=5, strategy='kmeans', encode='ordinal')
    )

    # Categorical preprocessor
    cat_pp = make_pipeline(
        SimpleImputer(strategy='most_frequent'),
        OneHotEncoder(sparse=False, handle_unknown='ignore')
    )

    logging.info('Create transformer...')

    # Column transformer
    # NOTE: Here since we're working with the column indices
    # we need to re-map them to fit the training dataset X
    preprocessor = make_column_transformer(
        (num_pp, [i for i in range(len(NUM_FEAT))]),
        (cat_pp, [i for i in range(len(NUM_FEAT), len(NUM_FEAT + CAT_FEAT))])
    )

    logging.info('Create model pipeline...')

    # Model pipeline
    model = make_pipeline(
        preprocessor,
        MODEL
    )

    logging.info('Split data...')

    X = data[:, features]
    y = [targ_conv.get(i[0]) for i in data[:, TARG_FEAT]]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42)

    logging.info('Train model...')

    # Fit model using pipeline
    model.fit(X_train, y_train)

    logging.info('Results...')
    y_pred = model.predict(X_test)

    f_score = f1_score(y_test, y_pred, average='macro')
    cm = confusion_matrix(y_test, y_pred)

    logging.info(f'F1 score: {f_score}')
    logging.info(f'Confusion matrix: \n{cm}')

    # Export results
    model_path = os.path.abspath(os.path.join(output_path, f'{model_name}_model.pkl'))
    with open(model_path, 'wb') as file:
        dill.dump((model, features, TARG_FEAT, targ_conv), file)

    logging.info(f'Output saved to: {model_path}')
