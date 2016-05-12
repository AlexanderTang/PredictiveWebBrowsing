import sys
import transform_data
import preprocessing as pre
import numpy as np
import setup_data
import transform_data_to_graph as to_graph


def main(argv=None):
    if argv is not None:
        get_cleaned_training_files(argv)



if __name__ == "__main__":
    main(sys.argv)
