# Daily Fantasy Golf Webscraper and Analysis

I like to play daily fantasy golf through FanDuel. Hopefully, generating solid models will help pick high performing players each week.

## Installation

Required dependencies (currently):

- Python (>=3.4)
- Numpy
- Pandas
- BeautifulSoup

## Project Motivation and Purpose

This project started as a means to webscrape the PGATour.com website for player/tournament/historical data and has evolved into a desire for a tool that can generate worthwhile dfs lineup suggestions. Understanding statistics in golf to find hidden correlations is of particular interest to me; adding in the desire to generate a highly capable draft lineup, and you get the purpose of this project.

## Files

**dfs_weekly.ipynb**: Week to week analysis of players available from different data sources to generate a weekly FanDuel lineup

**golf_analysis.ipynb**: Initial project file that explored difference sources for data.

**pgatour.ipynb**: Notebook to use for eventual project utilization. This notebook is now primarily used to test files/classes/functions that are located in the pga_data subfolder but will be the focal notebook once analysis is to be performed.

**pga_data/mapping.py**: File to be utilized for proper mapping between desired player or statistic and prepares for webpage request.

**pga_data/scrape.py**: Working with mapping.py, this file performs the page request and transforms data into basic pandas dataframe

## Licensing and Acknowledgements

Data currently comes from the [PGA Tour](https://www.pgatour.com/).
