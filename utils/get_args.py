import argparse


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n",
        "--network",
        required=True,
        type=str
    )
    # parser.add_argument(
    # )
    args = parser.parse_args()

    return vars(args)
