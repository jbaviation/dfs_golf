import pandas as pd
import numpy as np
import datetime as dt
import re
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

        # Initilize _data variable
        self._data = pd.DataFrame()


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

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        # Eventually create a _check_data(new_data) function here
        self._data = new_data
        
    def pull(self):
        """Function to pull data from pgatour.com and put into dataframe"""
        # Retreive data
        try:
            pulled_data = pd.read_html(self.url)[1]
        except:
            print("data cannot be properly retrieved from pgatour.com")
            return
        
        ## Clean up columns names and characters in the data
        # Replace %
        pulled_data.columns = [re.sub(r'\%','pct',nm) for nm in pulled_data.columns]

        # Replace non alpha-numeric characters
        pulled_data.columns = [re.sub(r'[^a-zA-Z0-9]+','_', nm).lower().strip('_')
                               for nm in pulled_data.columns]

        # Change specific columns names
        pulled_data = pulled_data.rename({'average': 'avg',
                                          'rank_last_week': 'ranklw', 
                                          'rank_this_week': 'rank',
                                          'highest_value': 'max',
                                          'lowest_value': 'min'}, axis=1)
        # Handle columns with rankings and ties
        int_cols = [col for col in pulled_data.columns if 'rank' in col]
        pulled_data[int_cols] = (pulled_data[int_cols]
                                 .replace(r'[T|t]','',regex=True)
                                 .astype('Int64'))

        # Print message
        self.data = pulled_data
        print("data successfully pulled!")
    

class player:
    pass


class shots:
    """This class is setup to provide a means for someone to request shot-wise data
       for all holes in every tournament.
    """

    

