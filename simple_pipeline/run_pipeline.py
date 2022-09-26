import argparse
import logging

from simple_pipeline.pipeline_utils import run_pipeline


# Set logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)5s][%(filename)s:%(lineno)d] %(message)s',
)
LOG = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser()

    required = parser.add_argument_group('required arguments')

    required.add_argument('--input_dir',
                          help='Input data directory',
                          dest='input_dir',
                          default='./simple_pipeline/data')

    required.add_argument('--output_dir',
                          help='Output directory',
                          dest='output_dir',
                          default='./simple_pipeline/output')

    required.add_argument('--model_name',
                          help='Selected model approach',
                          dest='model_name',
                          default='logistic')

    # Drop unknown arguments
    args, unknown = parser.parse_known_args()
    return args


if __name__ == '__main__':
    PARSER = _parse_args()

    LOG.info('Run training pipeline')

    run_pipeline(input_dir=PARSER.input_dir,
                 output_dir=PARSER.output_dir,
                 model_name=PARSER.model_name)

    LOG.info('Training pipeline finished!')
