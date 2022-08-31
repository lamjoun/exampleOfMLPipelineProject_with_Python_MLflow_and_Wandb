#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning,
exporting the result to a new artifact

AUTHOR: Rachid LAMJOUN

Date: August, 2022

Version: 1.0
"""
#
import pandas as pd
import argparse
import logging
import wandb
# import os


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    """
    Connection to W&B to retrieve the file to be processed by clean operations.
    The result file will be uploaded to W&B.
    The needed information will be passed through the args object.
    input:
            args: A configuration file hydra type
    output:
            None
    """
    #
    # Init conn with wandb
    run = wandb.init(job_type="basic_cleaning")

    # updating the run
    run.config.update(args)

    # retrieve Data
    logger.info("retrieve Data from W&B...")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    # Drop prices outliers
    logger.info("The Drop of outliers prices.")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    
    # Drop outliers for longitude and latitude columns
    logger.info("Drop outliers for longitude and latitude columns.")
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    #

    # Convert last_review column to datetime
    logger.info("Converting last_review column to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Saving the result in the temp_file without index
    logger.info("Saving the result in the temp_file without index")
    temp_file = args.output_artifact
    df.to_csv(temp_file, index=False)

    # output artifact object
    output_artifact_obj = wandb.Artifact(
                                args.output_artifact,
                                type=args.output_type,
                                description=args.output_description)
    #
    output_artifact_obj.add_file(temp_file)
    #
    # Store the artifact
    logger.info("Store the result file as artifact in W&B")
    run.log_artifact(output_artifact_obj)

    # remove temp_file
    # os.remove(temp_file)

    # Stop the run
    run.finish()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help='Input Artifact Name with version or tag: e.g. <artifact_name>:v3 or <artifact_name>:latest',
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help='Output Artifact Name to create',
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help='Type of the Output Artifact',
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help='Description of the Output Artifact',
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help='Min value for the price for cleaning',
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help='Max value for the price for cleaning',
        required=True
    )

    args = parser.parse_args()

    go(args)
