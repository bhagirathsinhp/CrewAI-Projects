#!/usr/bin/env python
import sys
import warnings
import os
from dotenv import load_dotenv

load_dotenv(override=True)

from datetime import datetime
from financial_researcher.crew import FinancialResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the financial researcher crew.
    """
    inputs = {
        'company': 'Tesla',
        'current_year': str(datetime.now().year)
    }

    try:
        result = FinancialResearcher().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()