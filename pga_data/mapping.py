import difflib

shots_gained_map = {'SG: Total': '02675',
                    'SG: Tee to Green': '02674',
                    'SG: Off the Tee': '02567',
                    'SG: Approach the Green': '02568',
                    'SG: Around the Green': '02569',
                    'SG: Putting': '02564'
                   }

off_the_tee_map = {'Driving Distance': '101',
                   'Longest Drives': '159',
                   'Driving Percentage 320+': '496',
                   'Driving Percentage 300-320': '495',
                   'Driving Percentage 300+': '454',
                   'Driving Percentage 280-300': '455',
                   'Driving Percentage 260-280': '456',
                   'Driving Percentage 240-260': '457',
                   'Driving Percentage <=240': '458',
                   'Percentage of Yardage Covered by Tee Shots': '02341',
                   'Percentage of Yardage Covered by Tee Shots Par 4s': '02342',
                   'Percentage of Yardage Covered by Tee Shots Par 5s': '02343',
                   'Driving Accuracy Percentage': '102',
                   'Rough Tendency': '02435',
                   'Left Rough Tendency': '459',
                   'Right Rough Tendency': '460',
                   'Left Rough Tendency (RTP Score)': '081',
                   'Right Rough Tendency (RTP Score)': '080',
                   'Fairway Bunker Tendency': '01008',
                   'Missed Fairway Percentage': '461',
                   'Hit Fairway Percentage': '213',
                   'Distance From Edge of Fairway': '02420',
                   'Distance From Center of Fairway': '02421',
                   'Left Tendency': '02422',
                   'Right Tendency': '02423',
                   'Good Drive Percentage': '02438',
                   'Total Driving': '129',
                   'Ball Striking': '158',
                   'Club Head Speed': '02401',
                   'Ball Speed': '02402',
                   'Smash Factor': '02403',
                   'Launch Angle': '02404',
                   'Spin Rate': '02405',
                   'Distance to Apex': '02406',
                   'Apex Height': '02407',
                   'Hang Time': '02408',
                   'Carry Distance': '02409',
                   'Carry Efficiency': '02410',
                   'Total Distance Efficiency': '02411',
                   'Total Driving Efficiency': '02412'
                  }

app_the_green_map = {'GIR Percentage': '103',
                     'Greens or Fringe in Regulation': '02437',
                     'GIR Percentage >200 Yards': '326',
                     'GIR Percentage 175-200 Yards': '327',
                     'GIR Percentage 150-175 Yards': '328',
                     'GIR Percentage 125-150 Yards': '329',
                     'GIR Percentage <125 Yards': '330',
                     'GIR Percentage 100-125 Yards': '077',
                     'GIR Percentage >100 Yards': '02332',
                     'GIR Percentage <100 Yards': '02330',
                     'GIR Percentage 75-100 Yards': '078',
                     'GIR Percentage <75 Yards': '079',
                     'GIR Percentage From Fairway': '190',
                     'GIR Percentage Fairway Bunker': '02434',
                     'GIR Percentage From Other Than Fairway': '199',
                    }

around_the_green_map = {}

putting_map = {}

scoring_map = {}

streaks_map = {}

finishes_map = {}

rankings_map = {} 

all_time_records_map = {}

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

def list_stats_from_keyword(keyword):
    """(Verified) Searches thru all stats and returns dictionary with {stat title: url number}
       based on the keyword provided."""
    all_stats_dict = combine_dicts(map_map.values())
    matches = {key: value for key, value in all_stats_dict.items() if keyword.lower() in key.lower()}
    return matches

def list_stats_from_cat(category='all'):
    """(Verified) Lists all available stats based on category or categories.
        
        args:
         category (list or string): {default='all', 'sg', 'ott', 'apr', 'arg', 'putt',
                                     'scoring', 'streaks', 'finishes', 'rankings', 'winning'}
    """
    if isinstance(category, list):
        matches = [v for c in category for k, v in map_map.items() if c.lower() in k]
        return combine_dicts(matches)
    elif category=='all':
        return combine_dicts(map_map.values())
    elif isinstance(category, str):
        match = [v for k, v in map_map.items() if category.lower() in k]
        return combine_dicts(match)
    else:
        raise KeyError(f'Cannot find {category} in list of recognized categories')

def list_stat(stat):
    """Function to find the relevent statistical category from the stat_search string.
        args: 
          stat (list or str) - statistic(s) to retrieve
    """
    # Get all stats
    all_stats = combine_dicts(map_map.values())
    
    if isinstance(stat, list):
        # Clean up the search in case of typos
        stats = [difflib.get_close_matches(s, all_stats.keys(), n=1)[0] for s in stat]
    elif isinstance(stat, str):
        # Clean up the search in case of typos
        stats = difflib.get_close_matches(stat, all_stats.keys(), n=1)[0]
    else:
        raise TypeError('Unknown type entered into function')

    # Return dictionary of matches
    return {key: val for key, val in all_stats.items() if key in stats}
    
def combine_dicts(list_of_dicts=[]):
    # In case list_of_dicts is a dict_value object, turn it into a list
    list_of_dicts = list(list_of_dicts)
    
    # Combine Dictionaries
    dict_combined = {}
    for d in list_of_dicts:
        dict_combined.update(d)
        
    # Return final dict
    return dict_combined