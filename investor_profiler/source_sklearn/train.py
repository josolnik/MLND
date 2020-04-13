import os
import argparse
import pandas as pd

# clustering algorithms
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

# save the model
from sklearn.externals import joblib


# Model load function
def model_fn(model_dir):
    """Load model from the model_dir. This is the same model that is saved
    in the main if statement.
    """
    print("Loading model.")

    # load using joblib
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    print("Done loading model.")

    return model

if __name__ == '__main__':
    # All of the model parameters and training parameters are sent as arguments
    # when this script is executed, during a training job

    # Here we set up an argument parser to easily access the parameters
    parser = argparse.ArgumentParser()

    # SageMaker parameters, like the directories for training data and saving models; set automatically
    parser.add_argument('--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--data-dir', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    # Define the number of clusters
    parser.add_argument('--num-clusters', type=int, default=3)

    # args holds all passed-in arguments
    args = parser.parse_args()

    # Read in csv training file
    training_dir = args.data_dir
    train_x = pd.read_csv(os.path.join(training_dir, "train.csv"), header=None, names=None)

    # define the nodel
    model = KMeans(n_clusters=args.num_clusters, random_state=0)

    # train the model
    model.fit(train_x)
    
    # save the trained model
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))