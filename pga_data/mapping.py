import difflib
import json
import os
from bs4 import BeautifulSoup
import requests
import time
import json
from pathlib import Path
import web_scraping_tools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import re

driver_loc = web_scraping_tools.get_chromedriver()


# Turn the functions below into a class so as to minimize the load on reading webpages
class mapping:
    """
    Attributes
    ==========
    player_meta     : list of dicts
                      Contains details needed from each player to be able to load player data
    stat_meta       : list of dicts
                      Contains details needed from each stat category to load specific stats
    tourney_meta    : dict
                      Contains years as keys and tournaments played as the values
    """
    def __init__(self, load_meta_locs=True):
        load_meta_status = self.load_metas() if load_meta_locs else 'Not Loaded'
    
    def load_metas(self):
        b_dir = 'pga_data/data_files'  # baseline directory for files
        json_files = ['tourney_meta', 'stat_meta', 'player_meta']  # files to load
        full_files = [os.path.join(b_dir, json_file+'.json') for json_file in json_files]  # combine dir and file

        # Loop thru each file and pull into json_files name
        for file, name in zip(full_files, json_files):
            with open(file, 'r') as read_file:
                setattr(self, name, json.load(read_file))
            
        return 'Loaded' 

    def list_stats_from_keyword(self, keyword, all_data=False):
        """(NEW Verified) Searches thru all stats and returns dictionary with {stat title: url number}
           based on the keyword provided."""
        if all_data:
            return [stat for stat in self.stat_meta if keyword.lower() in stat['stat name'].lower()]
        else:
            return [stat['stat name'] for stat in self.stat_meta if keyword.lower() in stat['stat name'].lower()]    

    def list_stats_from_cat(self, category='all', all_data=False):
        """(NEW Verified) Lists all available stats based on category or categories.

            args:
             category (list or string): {default='All', 
                                         'All-Time Records',
                                         'Approach the Green',
                                         'Around the Green',
                                         'Money/Finishes',
                                         'Off the Tee',
                                         'Points/Rankings',
                                         'Putting',
                                         'Scoring',
                                         'Shots Gained',
                                         'Streaks'}
        """
        if isinstance(category, list):
            matches = [stat for cat in category for stat in self.stat_meta 
                       if cat.lower() in stat['stat category'].lower()]
        elif category.lower()=='all':
            matches = self.stat_meta
        elif isinstance(category, str):
            matches = [stat for stat in self.stat_meta if category.lower() in stat['stat category'].lower()]
        else:
            raise KeyError(f'Cannot find {category} in list of recognized categories')

        r = matches if all_data else [stat['stat name'] for stat in matches]
        return r

    def list_stat(self, stat, from_id=False):
        """(NEW Verified) Function to find the relevent statistical category from the stat_search string.
            args: 
              stat (list or str) - statistic(s) to retrieve
              from_id (bool)     - search thru stat ids instead of stat name
        """
        option = 'stat id' if from_id else 'stat name'
        all_stats = [stat[option] for stat in self.stat_meta]
        
        if isinstance(stat, list):
            # Clean up the search in case of typos
            matches = [difflib.get_close_matches(s, all_stats, n=1)[0] for s in stat]
            return [d for d in self.stat_meta for m in matches if d[option]==m]
        elif isinstance(stat, str):
            # Clean up the search in case of typos
            matches = difflib.get_close_matches(stat, all_stats, n=1)[0]
            return [d for d in self.stat_meta if d[option]==matches][0]
        else:
            raise TypeError('Unknown type entered into function')
            


def combine_dicts(list_of_dicts=[]):
    # In case list_of_dicts is a dict_value object, turn it into a list
    list_of_dicts = list(list_of_dicts)
    
    # Combine Dictionaries
    dict_combined = {}
    for d in list_of_dicts:
        dict_combined.update(d)
        
    # Return final dict
    return dict_combined

####### Use the Following Functions for scraping data from pgatour.com ######
class stat_make_meta:
    """Class to make meta json files for easy reading of stat categories."""

    # Create function for finding years available for each stat
    def get_years(self, stat_id, soup=None):
        if soup is None:
            url = f'https://www.pgatour.com/stats/stat.{stat_id}.html'

            # Get page content
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

        select_class = "statistics-details-select statistics-details-select--season"
        select_class_alt = "statistics-details-select custom-page"

        # Website utilizes 2 different formats for selecting years
        try:
            years = sorted([int(opt.text) for opt in soup.find(class_=select_class).find_all('option')])
            issue1 = False
        except:
            issue1 = True
        try:
            years = sorted([int(opt.text) for opt in soup.find(class_=select_class_alt).find_all('option')])
            issue2 = False
        except:
            issue2 = True

        # If can't find years, assume none are available otherwise return from the try/except cases
        if (issue1 & issue2):
            return []
        else: 
            return years


    def get_tourney_dropdown(self, stat_id, soup=None):
        if soup is None:
            # check for dropdown of tournaments
            page = requests.get(f'https://www.pgatour.com/stats/stat.{stat_id}.html')
            soup = BeautifulSoup(page.content, 'html.parser')

        select_class = "statistics-details-select statistics-details-select--tournament"
        return soup.find(class_=select_class) is not None


    # Create function for finding tournaments/ids available for each stat
    def get_tourneys(self, stat_id, years=None, print_comments=False, check_for_dropdown=False):
        # Find years if no provided
        years = self.get_years(stat_id) if years is None else years

        # select tourney class data
        select_class = "statistics-details-select statistics-details-select--tournament"

        # loop thru years to create dict
        tourney_map = {}  # initialize the dictionary
        tourney_dropdown = self.get_tourney_dropdown(stat_id)
        print(f'Starting {stat_id}:\n Added', end=' ') if print_comments else None
        for year in years:
            url = f'https://www.pgatour.com/content/pgatour/stats/stat.{stat_id}.y{year}.html'

            # Get page content
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Create dict
            if tourney_dropdown:
                sub_dict = {opt['value']: opt.text for opt in soup.find(class_=select_class).find_all('option')}
            else:
                sub_dict = 'No Tournaments'

            # Add dict to tourney_map
            tourney_map[year] = sub_dict

            print(f'{year}', end=', ') if print_comments else None
            time.sleep(0.5)

        print(f'\nstat_id {stat_id} COMPLETE!!\n') if print_comments else None
        return tourney_map

    # Function for extracting data and putting into proper form for stat_meta
    def write_stat_meta(self, maps=None, cats=None):
        if maps is None:
            maps = [shots_gained_map,
                    off_the_tee_map,
                    app_the_green_map,
                    around_the_green_map,
                    putting_map,
                    scoring_map,
                    streaks_map,
                    finishes_map,
                    rankings_map,
                    all_time_records_map]
        if cats is None:
            cats = ['Shots Gained',
                    'Off the Tee',
                    'Approach the Green',
                    'Around the Green',
                    'Putting',
                    'Scoring',
                    'Streaks',
                    'Money/Finishes',
                    'Points/Rankings',
                    'All-Time Records']

        # Create new dictionary with years and tournaments as options
        all_map = {}
        for m, c in zip(maps, cats):
            print(f'Retrieving {c}...')
            sub_map = []
            for stat, stat_id in m.items():
                # Create soup object to reduce number of times website is accessed
                page = requests.get(f'https://www.pgatour.com/stats/stat.{stat_id}.html')
                soup = BeautifulSoup(page.content, 'html.parser')        

                # Append dictionary to list
                sub_map.append({'stat name': stat, 
                                'stat id': stat_id,
                                'stat category': c,
                                'years': self.get_years(stat_id, soup),
                                'tournament option': self.get_tourney_dropdown(stat_id, soup)
                               })
                print(f'  {stat}')
                time.sleep(5)
            print(f'...{c} COMPLETE!\n')
            all_map[c] = sub_map

        # Write mapped files above to output file
        with open('output.txt', 'w') as output:
             output.write(json.dumps(all_map))
                
                
    def make_player_meta(self, create_temp_file=True):
        """Function works to make the player_meta.json file"""
        import re
        page = requests.get('https://www.pgatour.com/players.html')
        soup = BeautifulSoup(page.content, 'html.parser')
        
        inactive_class = {'class': 'player-card'}
        active_class = {'class': 'player-card active'}

        img_pre = 'https://res.cloudinary.com/pga-tour/image/upload/c_fill,g_face:center,' + \
                  'h_294,q_auto,w_220/headshots_{}.png'
        list_players = []
        for player in soup.find_all('li', attrs=inactive_class):
            url = player.find(class_='player-link')['href']
            find_id = re.findall(r'player\.(\d+)\.', url)[0]
            player_dict = {'player last name': player.find(class_='player-surname').text,
                           'player first name': player.find(class_='player-firstname').text,
                           'player id': find_id,
                           'url': 'https://www.pgatour.com'+url,
                           'country': player.find(class_='player-country-title').text,
                           'active': False,
                           'image': img_pre.format(find_id)
                          }
            list_players.append(player_dict)
            
        for player in soup.find_all('li', attrs=active_class):
            url = player.find(class_='player-link')['href']
            find_id = re.findall(r'player\.(\d+)\.', url)[0]
            player_dict = {'player last name': player.find(class_='player-surname').text,
                           'player first name': player.find(class_='player-firstname').text,
                           'player id': find_id,
                           'url': 'https://www.pgatour.com'+url,
                           'country': player.find(class_='player-country-title').text,
                           'active': True,
                           'image': img_pre.format(find_id)
                          }
            list_players.append(player_dict)
            
        # Write to json
        insert_txt = '_temp' if create_temp_file else ''  # append temp to filename
        file = f'pga_data/data_files/player_meta{insert_txt}.json'

        with open(file, 'w') as output:
            json.dump(list_players, output, indent=6)
            print(f'{os.path.split(file)[-1]} has been created!')


class shot_make_meta:
    """Class to make meta json files for easy reading of schedule, round, and shot data."""

    def __make_tourney_links(self, season):
        """Gets specific season links.
        
        Parameters
        ----------
        season : str or int
            PGA Tour season. Some seasons consist of multiple years (i.e. 2020-2021), while others
            are individual years (i.e. 2013).  The inputed season must be an option on the season 
            dropdown of https://www.pgatour.com/schedule/
        """

        start_url = 'https://www.pgatour.com/schedule'
        base_url = 'https://www.pgatour.com'

        # Initiate webdriver
        s = Service(driver_loc)
        driver = webdriver.Chrome(service=s)
        driver.get(start_url)

        # Set view to full schedule
        button_id = 'menu-button-:rr:'
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, button_id)))
        except NoSuchElementException:
            raise NoSuchElementException(f'Dropdown for view is NOT FOUND')
        view_button = driver.find_element('id', button_id)
        view_button.click()

        button_id = 'menu-list-:rr:-menuitem-:ru:'
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, button_id)))
        except NoSuchElementException:
            raise NoSuchElementException(f'Dropdown for select view is NOT FOUND')
        full_schedule_button = driver.find_element('id', button_id)
        full_schedule_button.click()

        ## Set season to desired season
        # Select dropdown
        button_id = 'menu-button-:rd:'
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, button_id)))
        except NoSuchElementException:
            raise NoSuchElementException(f'Dropdown for select season is NOT FOUND')

        season_button = driver.find_element('id', button_id)
        season_button.click()

        # Read season options
        soup = BeautifulSoup(driver.page_source, 'lxml')
        season_buttons = soup.find(attrs={'id': 'menu-list-:rd:'}).find_all('button')
        buttons = {button.text: button.get('id') for button in season_buttons}
        """buttons is of form {year: id}"""

        # Confirm season is in buttons
        self.season_options = list(buttons.keys())
        # print(f'Season options include:\n{list(buttons.keys())}')
        if season not in buttons.keys():
            raise IndexError(f'Season "{season}" is not an option for this page.')

        # Select the correct season
        id_ = buttons[season]
        select_season_button = driver.find_element('id', id_)
        select_season_button.click()

        # Wait for page to change then, get the soup
        time.sleep(5)  # can't get other waits to work
        
        # Get tournament name and links from each tournament in view
        soup = BeautifulSoup(driver.page_source, 'lxml')

        class_1 = 'css-k8jakh'  # top level class
        class_2 = 'css-yor8sx'  # 2nd level class
        class_3 = 'css-0'       # 3rd level class
        class_4 = 'chakra-text css-vgdvwe'  # 4th level class

        # Set different class values if season is single year
        if re.search(r'^[0-9]{4}$', season):
            class_1 = 'css-k8jakh'
            class_2 = 'css-1x95lhs'
            class_3 = 'css-g0elqx'
            class_4 = 'chakra-text css-vgdvwe'

        tourneys = []
        for whole_season in soup.find(attrs={'class': class_1}).find_all(attrs={'class': class_2}):
            for tourney in whole_season.find_all(attrs={'class': class_3}):
                tourney_dict = {}   # initialize new tourney_dict

                # Attempt to get link
                try:
                    tourney_link = tourney.find_all('a', href=True)[0]['href']
                    if not re.search(r'^/tournaments/', tourney_link):
                        tourney_dict['tournament_link'] = None
                    else:
                        tourney_dict['tournament_link'] = base_url + tourney_link
                except (IndexError, AttributeError):
                    tourney_dict['tournament_link'] = None

                # Attempt to get tournament name
                try:
                    tourney_dict['tournament_name'] = tourney.find(attrs={'class': class_4}).text
                except (IndexError, AttributeError):
                    tourney_dict['tournament_name'] = None

                # Pass if all values are none
                if not any(tourney_dict.values()):
                    continue
                tourneys.append(tourney_dict)

        # Closeout driver
        driver.quit()
       
        return tourneys
    

    def make_tourney_links(self, seasons, create_file=True):
        """Function to get all tourney links for all inputted seasons.
        
        Parameters
        ----------
        seasons : list of [str or int]
            List of PGA Tour seasons which are to be combined. Some seasons consist of multiple 
            years (i.e. 2020-2021), while others are individual years (i.e. 2013).  The inputed 
            season must be an option on the season dropdown of https://www.pgatour.com/schedule/
        create_file : bool, default=True
            Whether or not to create a json file.  Defaulted to true as a precaution. When this is
            set to false, any existing data file will be overwritten.
        """
        # Extend each tourney links
        tourney_links = []
        for season in seasons:
            tourney_links.extend(self.__make_tourney_links(season))

        # Output file
        if create_file:
            base_path = Path('pga_data/data_files/')
            file = base_path / 'tourney_links.json'
            with open(file, 'w') as f:
                json.dump(tourney_links, f, indent=6)
                print(f'{os.path.split(file)[-1]} has been created!')

        # Return list of all tournament links
        return tourney_links
