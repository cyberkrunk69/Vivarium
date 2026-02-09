import logging
from typing import List
import re
from . import utils  # Removed circular import

def auto_tag(text):
    # Auto-tag the text
    return tagging.tag(text)