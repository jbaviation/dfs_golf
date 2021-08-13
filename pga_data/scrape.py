import pandas as pd
import numpy as np
import datetime as dt
import pga_data.mapping as mapping

class stat:
    def __init__(self, stat='', from_id=False, season=dt.datetime.now().year, tournament=None, just_tournament=False):
        """This class is setup to provide a means for someone to request a particular stat and then
        it returns the url from PGATour.com to access the data.
           args:
             stat (str)             - statistics to retrieve
             from_id (str)          - use stat as 'stat id' rather than 'stat name'
             season (datetime)      - for specific seasons (NOT WORKED ON YET)
             tournament (str)       - specify tournament if not whole season is desired
             just_tournament (bool) - True for only tournament data False for season upto tourney
        """
        
        # Generate instance of necessary classes/variables
        self.from_id = from_id
        self.season = season
        self.tournament = tournament
        self.just_tournament = just_tournament
        self.meta = mapping.mapping()
               
        # Write necessary inputs to self (new way)
        self._stat = self._check_stat(stat)
    
        # Set url for initial class conditions
        self._set_url()


    def _check_stat(self, stat):
        """Primary purpose is to confirm that tournament, or year requested exists in particular stat."""
        check_stat = self.meta.list_stat(stat, self.from_id)
        
        # todo: confirm that year and tournament are available in the meta data
        return check_stat
        
        
    def _set_url(self):
        '''Function to be called whenever statistic, season, time period, or tournament 
           has been changed.  For now this function just accepts seasons and categories.'''

        # Find season to determine base_url
        this_year = dt.datetime.now().year  # for now set this to be calendar year, eventually will be seasons
        if self.season == this_year:
            # Set url for current season
            base_url = 'https://www.pgatour.com/stats/stat.{}.html'
            self.url = base_url.format(self.stat['stat id'])
        else:
            # Set url for entire alternate season
            base_url = 'https://www.pgatour.com/content/pgatour/stats/stat.{}.y{}.html'
            self.url = base_url.format(self.stat['stat id'], self.season)
            
   
    @property
    def stat(self):
        # stat is now a dictionary
        return self._stat
    
    @stat.setter
    def stat(self, new_stat):
        # stat is now a dictionary
        self._stat = self._check_stat(new_stat)
        self._set_url()
        
    def pull(self):
        """Function to pull data from pgatour.com and put into dataframe"""
        return pd.read_html(self.url)[1]
    

class player:
    pass

