import pandas as pd
import numpy as np
import datetime as dt
import pga_data.mapping as mapping

class stat:
    def __init__(self, stat='', stat_id='0', season=dt.datetime.now().year, thru_tournament=None):
        """This class is setup to provide a means for someone to request a particular stat and then
        it returns the url from PGATour.com to access the data."""
        
        # Write input values to self
        self._stat, self._stat_id = self._update_stat(stat, str(stat_id))
               
        # Set url for initial class conditions
        self.season = dt.datetime.now().season
        self.thru_tournament = thru_tournament
        self._set_url()

        
    def _update_stat(self, stat, stat_id='0'):
        # Look for if stat_id exists
        if str(stat_id) in list(mapping.list_stats_from_cat().values()):
            # Set stat and stat_id if stat_id matches what is in the full stat list
            new_stat, new_stat_id = list({k: v for k, v in mapping.list_stats_from_cat().items() 
                                            if v==str(stat_id)}.items())[0]
        else:
            # Use statistical_category to set cat and cat_id
            new_stat, new_stat_id = list(mapping.list_stat(stat).items())[0]
        
        return new_stat, new_stat_id
        
        
    def _set_url(self):
        '''Function to be called whenever statistic, season, time period, or tournament 
           has been changed.  For now this function just accepts seasons and categories.'''

        # Find season to determine base_url
        this_year = dt.datetime.now().year  # for now set this to be calendar year, eventually will be seasons
        if self.season == this_year:
            # Set url for current season
            base_url = 'https://www.pgatour.com/stats/stat.{}.html'
            self.url = base_url.format(self.stat_id)
        else:
            # Set url for entire alternate season
            base_url = 'https://www.pgatour.com/content/pgatour/stats/stat.{}.y{}.html'
            self.url = base_url.format(self.stat_id, self.season)
            
   
    @property
    def stat(self):
        return self._stat
    
    @stat.setter
    def stat(self, new_stat):
        self._stat, self._stat_id = self._update_stat(stat=new_stat)
        self._set_url()
        
    @property
    def stat_id(self):
        return self._stat_id
    
    @stat_id.setter
    def stat_id(self, new_stat_id):
        self._stat, self._stat_id = self._update_stat(stat=None, stat_id=str(new_stat_id))
        self._set_url()
        
    @property
    def category(self):
        """Define a category variable for easier readability"""
        return self.stat
    
    def pull(self):
        """Function to pull data from pgatour.com and put into dataframe"""
        return pd.read_html(self.url)[1]
    



