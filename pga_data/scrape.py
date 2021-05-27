import pandas as pd
import numpy as np
import pga_data.mapping

class stat:
    def __init__(self, statistical_category):
        """This class is setup to provide a means for someone to request a particular stat and then              it returns the url from PGATour.com to access the data."""
        self._cat, self._url_number = pga_data.mapping.interpret_category(statistical_category)
        
        # Set base url for whenever url_number changes
        self.base_url = 'https://www.pgatour.com/stats/stat.{}.html'
        
        # Set url
        self.url = self.base_url.format(self._url_number)
        
    @property
    def cat(self):
        return self._cat
    
    @cat.setter
    def cat(self, new_cat):
        self._cat, self.url_number = pga_data.mapping.interpret_category(new_cat)
        
    @property
    def category(self):
        """Define a category variable for easier readability"""
        return self.cat
    
    @property
    def url_number(self):
        return self._url_number
    
    @url_number.setter
    def url_number(self, new_url):
        self._url_number = new_url
        self.url = self.base_url.format(self._url_number)
        
    def pull(self):
        """Function to pull data from pgatour.com and put into dataframe"""
        return pd.read_html(self.url)[1]


