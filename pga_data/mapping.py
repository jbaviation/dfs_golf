import difflib
import json

with open('pga_data/data_files/tourney_meta.json', 'r') as read_file:
    tourney_meta = json.load(read_file)

with open('pga_data/data_files/stat_meta.json', 'r') as read_file:
    stat_meta = json.load(read_file)

    
shots_gained_map = {'SG: Total': '02675',
                    'SG: Tee to Green': '02674',
                    'SG: Off the Tee': '02567',
                    'SG: Approach the Green': '02568',
                    'SG: Around the Green': '02569',
                    'SG: Putting': '02564'
                   }

map_map = {'shots gained (sg)': shots_gained_map,
           'off the tee (ott)': off_the_tee_map,
           'approach the green (apr, app)': app_the_green_map,
           'around the green (arg)': around_the_green_map,
           'putting': putting_map,
           'scoring': scoring_map,
           'streaks': streaks_map,
           'finishes money earnings': finishes_map,
           'rankings points': rankings_map,
           'records winning': all_time_records_map}

def list_stats_from_keyword(keyword, all_data=False):
    """(NEW Verified) Searches thru all stats and returns dictionary with {stat title: url number}
       based on the keyword provided."""
    if all_data:
        return [stat for stat in stat_meta if keyword.lower() in stat['stat name'].lower()]
    else:
        return [stat['stat name'] for stat in stat_meta if keyword.lower() in stat['stat name'].lower()]

def list_stats_from_cat(category='all', all_data=False):
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
        matches = [stat for cat in category for stat in stat_meta 
                   if cat.lower() in stat['stat category'].lower()]
    elif category.lower()=='all':
        matches = stat_meta
    elif isinstance(category, str):
        matches = [stat for stat in stat_meta if category.lower() in stat['stat category'].lower()]
    else:
        raise KeyError(f'Cannot find {category} in list of recognized categories')
        
    r = matches if all_data else [stat['stat name'] for stat in matches]
    return r

def list_stat(stat):
    """(NEW Verified) Function to find the relevent statistical category from the stat_search string.
        args: 
          stat (list or str) - statistic(s) to retrieve
    """
    all_stats = [stat['stat name'] for stat in stat_meta]

    if isinstance(stat, list):
        # Clean up the search in case of typos
        matches = [difflib.get_close_matches(s, all_stats, n=1)[0] for s in stat]
        return [d for d in stat_meta for m in matches if d['stat name']==m]
    elif isinstance(stat, str):
        # Clean up the search in case of typos
        matches = difflib.get_close_matches(stat, all_stats, n=1)[0]
        return [d for d in stat_meta if d['stat name']==matches][0]
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
# import statements (comment out when not using)
from bs4 import BeautifulSoup
import requests
import time

# Create function for finding years available for each stat
def get_years(stat_id, soup=None):
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

def get_tourney_dropdown(stat_id, soup=None):
    if soup is None:
        # check for dropdown of tournaments
        page = requests.get(f'https://www.pgatour.com/stats/stat.{stat_id}.html')
        soup = BeautifulSoup(page.content, 'html.parser')
    
    select_class = "statistics-details-select statistics-details-select--tournament"
    return soup.find(class_=select_class) is not None

# Create function for finding tournaments/ids available for each stat
def get_tourneys(stat_id, years=None, print_comments=False, check_for_dropdown=False):
    # Find years if no provided
    years = get_years(stat_id) if years is None else years

    # select tourney class data
    select_class = "statistics-details-select statistics-details-select--tournament"
    
    # loop thru years to create dict
    tourney_map = {}  # initialize the dictionary
    tourney_dropdown = get_tourney_dropdown(stat_id)
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
def write_stat_meta(maps=None, cats=None):
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
                            'years': get_years(stat_id, soup),
                            'tournament option': get_tourney_dropdown(stat_id, soup)
                           })
            print(f'  {stat}')
            time.sleep(5)
        print(f'...{c} COMPLETE!\n')
        all_map[c] = sub_map

    # Write mapped files above to output file
    with open('output.txt', 'w') as output:
         output.write(json.dumps(all_map))