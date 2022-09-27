import os
import argparse
import logging

from training_pipeline.pipeline_utils import run_pipeline


def _parse_args():
    parser = argparse.ArgumentParser()

    required = parser.add_argument_group('required arguments')

    required.add_argument('--input_dir',
                          help='Input data directory',
                          dest='input_dir',
                          default='./training_pipeline/data')

    required.add_argument('--output_dir',
                          help='Output directory',
                          dest='output_dir',
                          default='./training_pipeline/output')

    required.add_argument('--model_name',
                          help='Selected model approach',
                          dest='model_name',
                          default='logistic')

    # Drop unknown arguments
    args, unknown = parser.parse_known_args()
    return args


if __name__ == '__main__':
    # Parse input arguments
    PARSER = _parse_args()

    # Set logging configuration
    LOG_PATH = os.path.abspath(os.path.join(f'./logging/{PARSER.model_name}.log'))
    logging.basicConfig(format='[%(asctime)s][%(levelname)5s][%(filename)s:%(lineno)d] %(message)s',
                        level=logging.INFO,
                        handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],)
    LOG = logging.getLogger(__name__)

    LOG.info('Run training pipeline')

    # Start training pipeline
    run_pipeline(input_dir=PARSER.input_dir,
                 output_dir=PARSER.output_dir,
                 model_name=PARSER.model_name)

    LOG.info('Training pipeline finished!')
