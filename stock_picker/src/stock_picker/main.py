#!/usr/bin/env python
import sys
import warnings
import os
from dotenv import load_dotenv

load_dotenv(override=True)

from datetime import datetime

from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'sector': 'Technology',
        'current_year': str(datetime.now().year)
    }

    try:
        result =StockPicker().crew().kickoff(inputs=inputs)
        print("\n\n=== FINAL DECISION ===\n\n")
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()
