import sys

from .DlMarkupApplication import DlMarkupApplication


def main():
    app = DlMarkupApplication(sys.argv)
    sys.exit(app.run())
