import sys

from .DlMarkupApplication import DlMarkupApplication


def main():
    """Entry point."""
    app = DlMarkupApplication(sys.argv)
    sys.exit(app.run())
