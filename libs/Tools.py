"""This class has various tools to help in the processing of info"""
import re

class Tools:
    """Tools to help website with human context."""
    
    def parseOutReleaseIds(self,id_string):
        regex_validate_string = r'\d{4,}'
        validator = re.compile(regex_validate_string)
        print validator.findall(id_string)
        
        return validator.findall(id_string)