import difflib

site_map = {'SG: Total': '02675',
            'SG: Tee to Green': '02674',
            'SG: Off the Tee': '02567',
            'SG: Approach the Green': '02568',
            'SG: Around the Green': '02569',
            'SG: Putting': '02564'
            }

def interpret_category(statistical_category):
    """This function takes a statistic string that is input from the user and interpret's which              data is being requested."""
    cat = difflib.get_close_matches(statistical_category, site_map.keys(), n=1)[0]
    url = site_map[cat]
    
    return cat, url