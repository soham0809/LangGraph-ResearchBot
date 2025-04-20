"""Configuration utilities for the dual-agent AI research system."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file (but not required)
load_dotenv()

# Set default parameters
MAX_SEARCH_RESULTS = 5
SEARCH_TIMEOUT = 10  # seconds 