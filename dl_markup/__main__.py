import sys
import argparse

from .DLMarkupApplication import DLMarkupApplication

parser = argparse.ArgumentParser(description='Markup tool for deep learning')
parser.add_argument(
    '--input_dir',
    default='./',
    help='Input directory for images')
parser.add_argument(
    '--output_dir',
    default='./',
    help='Output directory for marked images')


def main():
    """Entry point."""
    args = parser.parse_args()
    print(args)
    app = DLMarkupApplication(args.__dict__)
    sys.exit(app.run())
