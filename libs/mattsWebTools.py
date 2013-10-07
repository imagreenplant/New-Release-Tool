#!/usr/bin/env python

import textwrap

class MattsWebTools:
    """ Matts web tools contains a few functions for making the display of html better.  One example is the \
truncate function to help truncate text fields for display."""
    
    def truncate(self, text, max_size):
        if len(text) <= max_size:
            return text
        return textwrap.wrap(text, max_size-3)[0] + "..."