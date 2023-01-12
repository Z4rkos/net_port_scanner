import argparse


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n",
        "--network",
        required=True,
        type=str
    )
    parser.add_argument(
        "-p",
        "--ports",
        required=False,
        type=str,
        choices=["all", "well_known", "minimal"],
        default="minimal"
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=30
    )

    args = parser.parse_args()

    return vars(args)
