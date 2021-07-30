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
                     'Proximity To Hole': '331',
                     'Approaches From >275 Yards': '02361',
                     'Approaches From 250-275 Yards': '02360',
                     'Approaches From 225-250 Yards': '02359',
                     'Approaches From 200-225 Yards': '02358',
                     'Approaches From >200 Yards': '336',
                     'Approaches From 175-200 Yards': '337',
                     'Approaches From 150-175 Yards': '338',
                     'Approaches From 125-150 Yards': '339',
                     'Approaches From 100-125 Yards': '074',
                     'Approaches From 50-125 Yards': '340',
                     'Approaches From 75-100 Yards': '075',
                     'Approaches From 50-75 Yards': '076',
                     'Approaches From <100 Yards': '02329',
                     'Approaches From >100 Yards': '02331',
                     'Fairway Proximity': '431',
                     'Approaches From >275 Yards (Rough)': '02375',
                     'Approaches From 250-275 Yards (Rough)': '02374',
                     'Approaches From 225-250 Yards (Rough)': '02373',
                     'Approaches From 200-225 Yards (Rough)': '02372',
                     'Approaches From >200 Yards (Rough)': '02369',
                     'Approaches From 175-200 Yards (Rough)': '02368',
                     'Approaches From 150-175 Yards (Rough)': '02367',
                     'Approaches From 125-150 Yards (Rough)': '02366',
                     'Approaches From 100-125 Yards (Rough)': '02364',
                     'Approaches From 50-125 Yards (Rough)': '02365',
                     'Approaches From 75-100 Yards (Rough)': '02363',
                     'Approaches From 50-75 Yards (Rough)': '02362',
                     'Approaches From <100 Yards (Rough)': '02370',
                     'Approaches From >100 Yards (Rough)': '02371',
                     'Rough Proximity': '437',
                     'Left Rough Proximity': '432',
                     'Right Rough Proximity': '433',
                     'Birdie or Better Percentage Fairway': '02333',
                     'Birdie or Better Percentage Left Rough': '02334',
                     'Birdie or Better Percentage Right Rough': '02335',
                     'Birdie or Better Percentage Rough': '02336',
                     'Birdie or Better Percentage >200 Yards': '357',
                     'Birdie or Better Percentage 175-200 Yards': '358',
                     'Birdie or Better Percentage 150-175 Yards': '359',
                     'Birdie or Better Percentage 125-150 Yards': '360',
                     'Birdie or Better Percentage <125 Yards': '361',
                     'Approaches From >275 Yards (RTP)': '02379',
                     'Approaches From 250-275 Yards (RTP)': '02378',
                     'Approaches From 225-250 Yards (RTP)': '02377',
                     'Approaches From 200-225 Yards (RTP)': '02376',
                     'Approaches From >200 Yards (RTP)': '480',
                     'Approaches From 175-200 Yards (RTP)': '479',
                     'Approaches From 150-175 Yards (RTP)': '478',
                     'Approaches From 125-150 Yards (RTP)': '473',
                     'Approaches From <125 Yards (RTP)': '472',
                     'Approaches From 100-125 Yards (RTP)': '028',
                     'Approaches From 75-100 Yards (RTP)': '029',
                     'Approaches From 50-75 Yards (RTP)': '030',
                     'Approaches From 50-75 Yards (Rough, RTP)': '02380',
                     'Approaches From 75-100 Yards (Rough, RTP)': '02381',
                     'Approaches From 100-125 Yards (Rough, RTP)': '02382',
                     'Approaches From <125 Yards (Rough, RTP)': '02383',
                     'Approaches From 125-150 Yards (Rough, RTP)': '02384',
                     'Approaches From 150-175 Yards (Rough, RTP)': '02385',
                     'Approaches From 175-200 Yards (Rough, RTP)': '02386',
                     'Approaches From >200 Yards (Rough, RTP)': '02387',
                     'Approaches From <100 Yards (Rough, RTP)': '02388',
                     'Approaches From >100 Yards (Rough, RTP)': '02389',
                     'Approaches From 200-225 Yards (Rough, RTP)': '02390',
                     'Approaches From 225-250 Yards (Rough, RTP)': '02391',
                     'Approaches From 250-275 Yards (Rough, RTP)': '02392',
                     'Approaches From >275 Yards (Rough, RTP)': '02393',
                     'Approaches From Left Rough (RTP)': '469',
                     'Approaches From Right Rough (RTP)': '470',
                     'Approaches From Fairway (RTP)': '471',
                     'Going For The Green': '419',
                     'Going For The Green - Hit Green Percentage': '486',
                     'Going For The Green - Birdie or Better': '02357',
                     'Going For The Green - Par 5': '436',
                     'Going For The Green - Average Yardage': '02426',
                     'Going For The Green - Average Yardage Remaining': '02431',
                     'Total Hole Outs': '350',
                     'Longest Hole Out': '351',
                     'Average Approach Distance': '02325',
                     'Average Approach Distance - Birdie or Better': '02338',
                     'Average Approach Distance - Par': '02339',
                     'Average Approach Distance - Bogey or Worse': '02340',
                     'Average Approach Distance From Tee Shot': '02430'
                    }

around_the_green_map = {'Sand Save Percentage': '111',
                        'Sand Save Percentage From >30 Yards': '370',
                        'Sand Save Percentage From 20-30 Yards': '371',
                        'Sand Save Percentage From 10-20 Yards': '372',
                        'Sand Save Percentage From <10 Yards': '373',
                        'Scrambling': '130',
                        'Scrambling From The Sand': '362',
                        'Scrambling From The Rough': '363',
                        'Scrambling From The Fringe': '364',
                        'Scrambling From Other Locations': '365',
                        'Scrambling From >30 Yards': '366',
                        'Scrambling From 20-30 Yards': '367',
                        'Scrambling From 10-20 Yards': '368',
                        'Scrambling From <10 Yards': '369',
                        'Proximity To Hole (ARG)': '374',
                        'Proximity To Hole From The Sand': '375',
                        'Proximity To Hole From The Fringe': '377',
                        'Proximity To Hole From The Rough': '376',
                        'Proximity To Hole From Other Locations': '378',
                        'Proximity To Hole From >30 Yards': '379',
                        'Proximity To Hole From 20-30 Yards': '380',
                        'Proximity To Hole From 10-20 Yards': '381',
                        'Proximity To Hole From <10 Yards': '382',
                        'Scrambling - Average Distance To Hole': '481',
                        'Scrambling >30 Yards (RTP)': '466',
                        'Scrambling 20-30 Yards (RTP)': '467',
                        'Scrambling 10-20 Yards (RTP)': '468',
                        'Scrambling From The Fringe (RTP)': '465',
                        'Scrambling From The Rough (RTP)': '464'
                       }

putting_map = {'One-Putt Percentage': '413',
               'One-Putt Percentage - Round 1': '414',
               'One-Putt Percentage - Round 2': '415',
               'One-Putt Percentage - Round 3': '416',
               'One-Putt Percentage - Round 4': '417',
               'One-Putt Percentage - Round 5': '418',
               'Total One-Putts <5 Feet': '420',
               'Total One-Putts 5-10 Feet': '421',
               'Total One-Putts 10-15 Feet': '422',
               'Total One-Putts 15-20 Feet': '423',
               'Total One-Putts 20-25 Feet': '424',
               'Total One-Putts >25 Feet': '425',
               'One-Putts Per Round': '398',
               'Longest Putts': '498',
               'Three-Putt Avoidance': '426',
               'Three-Putt Avoidance - Round 1': '427',
               'Three-Putt Avoidance - Round 2': '428',
               'Three-Putt Avoidance - Round 3': '429',
               'Three-Putt Avoidance - Round 4': '430',
               'Three-Putt Avoidance - Round 5': '440',
               'Three-Putt Avoidance <5 Feet': '068',
               'Three-Putt Avoidance 5-10 Feet': '069',
               'Three-Putt Avoidance 10-15 Feet': '070',
               'Three-Putt Avoidance 15-20 Feet': '145',
               'Three-Putt Avoidance 20-25 Feet': '146',
               'Three-Putt Avoidance >25 Feet': '147',
               'Total Three-Putts <5 Feet': '441',
               'Total Three-Putts 5-10 Feet': '442',
               'Total Three-Putts 10-15 Feet': '443',
               'Total Three-Putts 15-20 Feet': '444',
               'Total Three-Putts 20-25 Feet': '445',
               'Total Three-Putts >25 Feet': '446',
               'Three-Putts Per Round': '400',
               'Three-Putts or Greater Per Round': '401',
               'Putts Made From >25 Feet': '408',
               'Putts Made From >20 Feet': '02429',
               'Putts Made From 15-25 Feet': '02328',
               'Putts Made From 20-25 Feet': '407',
               'Putts Made From 15-20 Feet': '406',
               'Putts Made From 5-15 Feet': '02327',
               'Putts Made From 10-15 Feet': '405',
               'Putts Made From <10 Feet': '484',
               'Putts Made From 5-10 Feet': '404',
               'Putts Made From 3-5 Feet': '02427',
               'Putts Made From <5 Feet': '403',
               'Putts Made From 10 Feet': '348',
               'Putts Made From 9 Feet': '347',
               'Putts Made From 8 Feet': '346',
               'Putts Made From 7 Feet': '345',
               'Putts Made From 6 Feet': '344',
               'Putts Made From 5 Feet': '343',
               'Putts Made From >10 Feet': '356',
               'Putts Made From 4-8 Feet': '485',
               'Putts Made From 4 Feet': '342',
               'Putts Made From 3 Feet': '341',
               'Putts Made From >10 Feet Per Event': '434',
               'Putts Made From >20 Feet Per Event': '435',
               'GIR Average Putts From >35 Feet': '073',
               'GIR Average Putts From 30-35 Feet': '072',
               'GIR Average Putts From 25-30 Feet': '071',
               'GIR Average Putts From >25 Feet': '388',
               'GIR Average Putts From 20-25 Feet': '387',
               'GIR Average Putts From 15-20 Feet': '386',
               'GIR Average Putts From 10-15 Feet': '385',
               'GIR Average Putts From 5-10 Feet': '384',
               'GIR Average Putts From <5 Feet': '383',
               'Putts Per Round': '119',
               'Putts Per Round - Round 1': '393',
               'Putts Per Round - Round 2': '394',
               'Putts Per Round - Round 3': '395',
               'Putts Per Round - Round 4': '396',
               'Putts Per Round - Round 5': '397',
               'Two-Putts Per Round': '399',
               'Total Putting': '02428',
               'Bonus Putting': '02439',
               'Putting Average': '104',
               'Overall Putting Average': '402',
               'Birdie or Better Conversion Percentage': '115',
               'Average Putt Distance - All One-Putts': '409',
               'Average Putt Distance - All Two-Putts': '410',
               'Average Putt Distance - All Three-Putts': '411',
               'Average Putt Distance - All >=Three-Putts': '412',
               'Average Putt Distance - GIR One-Putts': '389',
               'Average Putt Distance - GIR Two-Putts': '390',
               'Average Putt Distance - GIR Three-Putts': '391',
               'Average Putt Distance - GIR >=Three-Putts': '392',
               'Average Putt Distance of Putts Made': '438',
               'Average Putt Distance of Birdie Putts Made': '02440',
               'Average Putt Distance of Eagle Putts Made': '02442',
               'Average Putts Made Distance': '135',
               'Average Approach Putt Performance': '349'
              }

scoring_map = {'Scoring Average': '120',
               'Scoring Average Actual': '108',
               'Scoring Average Before Cut': '116',
               'Stroke Differential Field Average': '02417',
               'Lowest Round': '299',
               'Rounds In The 60s': '152',
               'Sub-Par Rounds': '153',
               'Par 3 Birdie or Better': '112',
               'Par 4 Birdie or Better': '113',
               'Par 5 Birdie or Better': '114',
               'Par 4 Eagles': '447',
               'Par 5 Eagles': '448',
               'Eagle Frequency': '155',
               'Total Eagles': '106',
               'Par Breakers': '105',
               'Birdie Average': '156',
               'Total Birdies': '107',
               'Bounce Back': '160',
               'Birdie To Bogey Ratio': '02415',
               'Birdie or Better Percentage': '352',
               'Bogey Avoidance': '02414',
               'Reverse Bounce Back': '02416',
               'Bogey Average': '02419',
               'Scoring Average - Final Round': '118',
               'Scoring Average - Round 1': '148',
               'Scoring Average - Round 2': '149',
               'Scoring Average - Round 3': '117',
               'Scoring Average - Round 4': '285',
               'Scoring Average - Round 5': '286',
               'Scoring Average - Front 9 Round 1': '245',
               'Scoring Average - Front 9 Round 2': '253',
               'Scoring Average - Front 9 Round 3': '261',
               'Scoring Average - Front 9 Round 4': '269',
               'Scoring Average - Back 9 Round 1': '246',
               'Scoring Average - Back 9 Round 2': '254',
               'Scoring Average - Back 9 Round 3': '262',
               'Scoring Average - Back 9 Round 4': '270',
               'Performance - Final Round': '219',
               'Performance - Final Round Top 10': '220',
               'Performance - Final Round Top 5': '309',
               'Performance - Final Round 11-25': '310',
               'Performance - Final Round >25': '311',
               'Performance - Final Round 6-10': '453',
               'Performance - Par 3': '171',
               'Performance - Par 4': '172',
               'Performance - Par 5': '173',
               'Scoring Average - Par 3': '142',
               'Scoring Average - Par 4': '143',
               'Scoring Average - Par 5': '144',
               'Scoring Average - Par 3 Early': '223',
               'Scoring Average - Par 3 Late': '224',
               'Scoring Average - Par 4 Early': '231',
               'Scoring Average - Par 4 Late': '232',
               'Scoring Average - Par 5 Early': '239',
               'Scoring Average - Par 5 Late': '240',
               'Scoring Average - Front 9': '207',
               'Scoring Average - Front 9 Par 3': '221',
               'Scoring Average - Front 9 Par 4': '229',
               'Scoring Average - Front 9 Par 5': '237',
               'Lowest Round - Front 9': '301',
               'Scoring Average - Back 9': '208',
               'Scoring Average - Back 9 Par 3': '222',
               'Scoring Average - Back 9 Par 4': '230',
               'Scoring Average - Back 9 Par 5': '238',
               'Lowest Round - Back 9': '302',
               'Scoring Average - Early': '292',
               'Lowest Round - Early': '303',
               'Scoring Average - Late': '293',
               'Lowest Round - Late': '304',
               'Scoring Average - Early 1st Tee Start': '209',
               'Scoring Average - Early 1st Tee Start Par 3': '225',
               'Scoring Average - Early 1st Tee Start Par 4': '233',
               'Scoring Average - Early 1st Tee Start Par 5': '241',
               'Scoring Average - Late 1st Tee Start': '211',
               'Scoring Average - Late 1st Tee Start Par 3': '227',
               'Scoring Average - Late 1st Tee Start Par 4': '235',
               'Scoring Average - Late 1st Tee Start Par 5': '243',
               'Scoring Average - Early 1st Tee Start Round 1': '249',
               'Scoring Average - Early 1st Tee Start Round 2': '257',
               'Scoring Average - Early 1st Tee Start Round 3': '265',
               'Scoring Average - Early 1st Tee Start Round 4': '273',
               'Scoring Average - Late 1st Tee Start Round 1': '251',
               'Scoring Average - Late 1st Tee Start Round 2': '259',
               'Scoring Average - Late 1st Tee Start Round 3': '267',
               'Scoring Average - Late 1st Tee Start Round 4': '275',
               'Lowest Round - Early 1st Tee Start': '305',
               'Lowest Round - Late 1st Tee Start': '307',
               'Scoring Average - Early 10th Tee Start': '210',
               'Scoring Average - Early 10th Tee Start Par 3': '226',
               'Scoring Average - Early 10th Tee Start Par 4': '234',
               'Scoring Average - Early 10th Tee Start Par 5': '242',
               'Scoring Average - Late 10th Tee Start': '212',
               'Scoring Average - Late 10th Tee Start Par 3': '228',
               'Scoring Average - Late 10th Tee Start Par 4': '236',
               'Scoring Average - Late 10th Tee Start Par 5': '244',
               'Scoring Average - Early 10th Tee Start Round 1': '250',
               'Scoring Average - Early 10th Tee Start Round 2': '258',
               'Scoring Average - Early 10th Tee Start Round 3': '266',
               'Scoring Average - Early 10th Tee Start Round 4': '274',
               'Scoring Average - Late 10th Tee Start Round 1': '252',
               'Scoring Average - Late 10th Tee Start Round 2': '260',
               'Scoring Average - Late 10th Tee Start Round 3': '268',
               'Scoring Average - Late 10th Tee Start Round 4': '276',
               'Lowest Round - Early 10th Tee Start': '306',
               'Lowest Round - Late 10th Tee Start': '308',
               'Par 3 Efficiency <100 Yards': '02517',
               'Par 3 Efficiency 100-125 Yards': '02518',
               'Par 3 Efficiency 125-150 Yards': '02519',
               'Par 3 Efficiency 150-175 Yards': '02520',
               'Par 3 Efficiency 175-200 Yards': '02521',
               'Par 3 Efficiency 200-225 Yards': '02522',
               'Par 3 Efficiency 225-250 Yards': '02523',
               'Par 3 Efficiency >250 Yards': '02524',
               'Par 4 Efficiency <250 Yards': '02525',
               'Par 4 Efficiency 250-300 Yards': '02526',
               'Par 4 Efficiency 300-350 Yards': '02527',
               'Par 4 Efficiency 350-400 Yards': '02528',
               'Par 4 Efficiency 400-450 Yards': '02529',
               'Par 4 Efficiency 450-500 Yards': '02530',
               'Par 4 Efficiency >500 Yards': '02531',
               'Par 5 Efficiency <500 Yards': '02532',
               'Par 5 Efficiency 500-550 Yards': '02533',
               'Par 5 Efficiency 550-600 Yards': '02534',
               'Par 5 Efficiency 600-650 Yards': '02535',
               'Par 5 Efficiency >650 Yards': '02536'
              }

streaks_map = {'Consecutive Fairways Hit': '297',
               'Consecutive GIR': '298',
               'Consecutive Sand Saves': '296',
               'One-Putt or Better Streak (YTD)': '295',
               'Streak Without Three-Putt (Current)': '483',
               'Streak Without Three-Putt (YTD)': '294',
               'Rounds in 60s Streak': '474',
               'Sub-Par Rounds Streak': '476',
               'Par or Better Streak (Current)': '150',
               'Rounds in 60s Streak (YTD)': '475',
               'Sub-Par Rounds Streak (YTD)': '477',
               'Par or Better Streak (YTD)': '482',
               'Consecutive Par 3 Birdies': '449',
               'Consecutive Par 4 Birdies': '450',
               'Consecutive Par 5 Birdies': '451',
               'Consecutive Holes Below Par': '452',
               'Consecutive Birdies': '02672',
               'Consecutive Birdies/Eagles': '02673',
               'Consecutive Cuts': '122',
               'Consecutive Cuts (YTD)': '137'
              }

finishes_map = {'Official Money': '109',
                'Career Money': '110',
                'Career Earnings': '014',
                'Non-Member Earnings': '139',
                'Non-Member Official and WGC Earnings': '02677',
                'Fall Series Money': '02444',
                'FedEx Cup Bonus Money': '02396',
                'Money Per Event': '154',
                'Total Money': '194',
                'Percentage of Available Purse Won': '02337',
                'Percentage of Potential Money Won': '02447',
                'Top 10 Finishes': '138',
                'Victories': '300'
               }

rankings_map = {'FedEx Cup Regular Season Points': '02394',
                'FedEx Cup Playoff Points': '02395',
                'FedEx Cup Points Per Event': '02562',
                'Ryder Cup Points': '131',
                'PGA Championship Points': '132',
                "Presidents Cup Points (United States)": '140',
                'Presidents Cup Points (International)': '187',
                'Percentage of Potential Points Won - FedEx Cup Regular Season': '02448',
                'Percentage of Potential Points Won - FedEx Cup Playoff': '02449',
                'FedEx Cup Season Points For Non-Members': '02398',
                'Non-WGC FedEx Cup Season Points For Non-Members': '02667',
                'FedEx Cup Standings': '02671',
                'All-Around Ranking': '127',
                'FedEx Air and Ground': '02685',
                'FedEx Ground Top Performer': '02689',
                'AON Risk Reward Challenge': '02445',
                'RSM Birdies Fore Love': '02690',
                'Official World Golf Ranking': '186',
                'Power Rating': '085',
                'Accuracy Rating': '086',
                'Short Game Rating': '087',
                'Putting Rating': '088',
                'Scoring Rating': '02346',
                'Power Rating - Last 5 Events': '02347',
                'Accuracy Rating - Last 5 Events': '02348',
                'Short Game Rating - Last 5 Events': '02349',
                'Putting Rating - Last 5 Events': '02350',
                'Scoring Rating - Last 5 Events': '02351',            
                'Power Rating - Last 15 Events': '02352',
                'Accuracy Rating - Last 15 Events': '02353',
                'Short Game Rating - Last 15 Events': '02354',
                'Putting Rating - Last 15 Events': '02355',
                'Scoring Rating - Last 15 Events': '02356',
               } 

all_time_records_map = {'Most Career Wins': 'ATR727',
                        'Most Wins in One Season': 'ATR51',
                        'Most Wins in One Tournament': 'ATR71',
                        'Most Wins at One Course': 'ATR162',
                        'Most Wins by Season': 'ATR725',
                        'Longest Win Streak (Starts)': 'ATR50',
                        'Longest Win Streak (Weeks)': 'ATR726',
                        'Longest Win Streak (Tournament)': 'ATR160',
                        'First Two Career Wins in Same Tournament': 'ATR53',
                        'Most Consecutive Seasons With a Win': 'ATR49',
                        'Most Consecutive Seasons With a Win To Start Career': 'ATR897',
                        'Largest Winning Margin': 'ATR68',
                        'Largest Final Round Comeback': 'ATR65',
                        'Longest Time Between 1st and Last Wins at Same Tournament': 'ATR52',
                        'Longest Time Between 1st and 2nd Wins at Same Tournament': 'ATR159',
                        'Longest Time Between 1st and Last Wins': 'ATR55',
                        'Longest Time Between Wins': 'ATR75',
                        'Lowest 9 Hole Score': 'ATR17',
                        'Lowest 18 Hole Score': 'ATR11',
                        'Lowest Opening 36 Hole Score': 'ATR10',
                        'Lowest Consecutive 36 Hole Score': 'ATR35',
                        'Lowest Opening 54 Hole Score': 'ATR9',
                        'Lowest Consecutive 54 Hole Score': 'ATR365',
                        'Lowest Score 72 Hole Event': 'ATR6',
                        'Lowest Score 72 Hole Event (RTP)': 'ATR18',
                        'Most Birdies 72 Hole Event': 'ATR31',
                        # Major Championship Wins
                        'All Time Wins (Majors)': 'ATR81',
                        'Grand Slam Winners': 'ATR82',
                        'Longest Time Between 1st and 2nd Major Wins': 'ATR723',
                        # FedEx Cup
                        'Most Consecutive Weeks at Number 1 (FedEx Cup)': 'ATR891',
                        'Rookies to Lead FedEx Cup': 'ATR892',
                        'Winners of FedEx Cup, The Players, a Major, WGC': 'ATR893',
                        # Wins and Finishes: Winners by Age
                        'Youngest Winners': 'ATR61',
                        'Oldest Winners': 'ATR62',
                        'Most Wins Before Age 23': 'ATR57',
                        'Most Wins Before Age 30': 'ATR56',
                        'Most Wins Age 30s': 'ATR58',
                        'Most Wins Age >40': 'ATR59',
                        'Most Consecutive Tournaments Won Age 20s': 'ATR728',
                        'Oldest 1st Time Winners': 'ATR63',
                        'Youngest To Win 5 Tournaments': 'ATR60',
                        'Youngest To Win 10 Tournaments': 'ATR730',
                        'Youngest To Win a World Golf Championships Tournament': 'ATR731',
                        'Oldest To Win a World Golf Championships Tournament': 'ATR732',
                        # Wins and Finishes: Types of Winners
                        'Most 1st Time Winners in a Season': 'ATR54',
                        'Father and Son To Win': 'ATR733',
                        'Father and Son To Win Same Tournament': 'ATR898',
                        'Grandfather and Grandson To Win': 'ATR734',
                        'Brothers To Win': 'ATR735',
                        'Amateurs To Win': 'ATR64',
                        'Most Wins By a Lefty': 'ATR736',
                        '1st Time Winners': 'ATR894',
                        # Wins and Finishes: Top-10s
                        'Most Top 10s in a Season': 'ATR98',
                        'Most Top 10s in a Career': 'ATR97',
                        'Most Consecutive Top 10s': 'ATR737',
                        'Oldest To Finish Top 10': 'ATR106',
                        # Wins and Finishes: The Last Time
                        'Last To Win Back-To-Back Starts': 'ATR460',
                        'Last To Win First 2 Starts of Season': 'ATR461',
                        'Last To Win Back-To-Back Tournaments': 'ATR463',
                        'Last To Win 3 Consecutive Starts': 'ATR462',
                        'Last To Win 3 Consecutive Tournaments': 'ATR464',
                        'Last To Win 4 Consecutive Starts': 'ATR1001',
                        'Last To Win 4 Consecutive Tournaments': 'ATR465',
                        'Last To Successfully Defend a Title': 'ATR466',
                        'Last To Earn 1st 2 Wins in Same Tournament': 'ATR1002',
                        'Last To Earn 1st 3 Wins in Same Tournament': 'ATR468',
                        'Last To Earn 1st 2 Wins in Consecutive Tournaments': 'ATR469',
                        'Last To Earn 1st 2 Wins in Consecutive Starts': 'ATR1003',
                        'Last To Earn 1st 3 Wins in Consecutive Starts': 'ATR470',
                        'Last To Successfully Defend a Title the Week After Winning a Tournament': 'ATR472',
                        'Last Back-To-Back Tournaments With Successfull Title Defenses': 'ATR473',
                        'Last Wire-To-Wire Winner': 'ATR474',
                        'Last Rookie Wire-To-Wire Winner': 'ATR475',
                        'Last To Win Same Tournament, Back-To-Back, Wire-To-Wire': 'ATR476',
                        'Last Back-To-Back Tournaments Won Wire-To-Wire': 'ATR477',
                        'Last Rookie To Win': 'ATR478',
                        'Last Rookie To Win Twice in a Season': 'ATR479',
                        'Last Lefty To Win': 'ATR701',
                        'Last Tournament With Lefty Winner and Runner-Up': 'ATR480',
                        'Last Amateur To Win': 'ATR481',
                        'Last Monday Qualifier To Win': 'ATR69',
                        'Last Non-Member To Win': 'ATR483',
                        'Last Sponsor Exemption To Win': 'ATR485',
                        'Last Alternate To Win': 'ATR486',
                        'Last Special Temporary Member To Win': 'ATR487',
                        'Last Time 5 Consecutive 1st Time Winners': 'ATR488',
                        'Last To Win in 1st PGA Tour Start': 'ATR489',
                        'Last To Win in 1st Start as Official PGA Tour Member': 'ATR310',
                        'Last To Lose a Playoff One Week and Win a Tournament the Next': 'ATR491',
                        'Last To Win a Tournament One Week and Lose a Playoff the Next': 'ATR492',
                        'Last To Win Same Tournament in a Playoff in Consecutive Seasons': 'ATR493',
                        'Last To Win a Tournament a Season After Losing it in a Playoff': 'ATR494',
                        'Last Time 3 or More Consecutive Winners in their 40s': 'ATR495',
                        'Last Time 3 Consecutive European Winners': 'ATR703',
                        'Last To Win With Even-Par or Worse Score': 'ATR704',
                        'Last To Win With Even-Par or Worse Score (Non-Major)': 'ATR67',
                        'Last To Win Without a Birdie in the Final Round': 'ATR706',
                        'Last To Win With Over-Par Scores in Each of the Last 2 Rounds': 'ATR707',
                        'Last To Play 72 Holes Without a Bogey and Win': 'ATR708',
                        'Last To Play 72 Holes Without a Bogey and Not Win': 'ATR709',
                        'Last To Win 54 Hole Tournament Without a Bogey': 'ATR710',
                        'Last To Record a Score >=80 and Win': 'ATR711',
                        'Last To Win After Holing Final Shot From Off the Green': 'ATR712',
                        'Last To Win By Playing Final 2 Holes at Least 3-Under': 'ATR713',
                        'Last To Win By Playing Final 4 Holes at Least 5-Under': 'ATR714',
                        'Last To Win When Starting on 10th Hole in Final Round': 'ATR715',
                        'Last To Make the Cut on the Number and Win': 'ATR716',
                        'Last To Win With Wife as Caddie': 'ATR717',
                        'Last To Win With Sister as Caddie': 'ATR718',
                        'Last To Win With Brother as Caddie': 'ATR719',
                        'Last To Win With Father as Caddie': 'ATR720',
                        'Last To Be in Last Place After 1st Round and Finish Top 10': 'ATR721',
                        # Scoring Records: In-Round Scoring Records
                        'Longest Birdie Streak': 'ATR23',
                        'Longest Birdie/Eagle Streak': 'ATR25',
                        'Longest Birdie Streak To Win': 'ATR29',
                        # Scoring Records: Putting Records
                        'Fewest Putts For 18 Holes': 'ATR89',
                        'Fewest Putts For 72 Holes': 'ATR90',
                        'Fewest Putts For 9 Holes': 'ATR91',
                        # Scoring Records: The Last Time
                        'Last To Make Back-To-Back Eagles': 'ATR453',
                        'Last To Make Back-To-Back Eagles to Start a Round': 'ATR454',
                        'Last To Make 4 Eagles in One Round': 'ATR450',
                        'Last To Make a Triple Bogey in Final Round and Win': 'ATR455',
                        'Last To Make a Quadruple Bogey and Win': 'ATR456',
                        'Last To Make a Double Eagle and Hole-In-One in Same Round': 'ATR451',
                        'Last Time 2 Double Eagles in the Same Tournament': 'ATR457',
                        'Last To Make a Hole-In-One, Eagle-2, and Eagle-3 in the Same Tournament': 'ATR458',
                        'Last To Make a 2, 3, 4, 5 on Par 5s in the Same Round': 'ATR452',
                        'Last Amateur To Shoot <=60': 'ATR542',
                        'Last To Shoot His Age': 'ATR700',
                        # Major Championships: Age
                        'Youngest Major Winners': 'ATR83',
                        'Youngest To Win 3 Majors': 'ATR724',
                        'Oldest Major Winners': 'ATR84',
                        'Oldest 1st Time Major Winners': 'ATR738',
                        'Youngest To Play in The Masters': 'ATR739',
                        'Youngest To Play in The PGA Championship': 'ATR1004',
                        'Youngest To Play in The US Open': 'ATR1005',
                        'Youngest To Play in The Open Championship': 'ATR1006',
                        'Oldest To Make Cut in a Major': 'ATR105',
                        'Oldest To Finish Top 10 in a Major': 'ATR107',
                        # Major Championships: The Last Time
                        'Last To Win Consecutive Tournaments (Including a Major)': 'ATR86',
                        'Last To Win Multiple Majors in Same Season': 'ATR743',
                        'Last To Successfully Defend Title at a Major': 'ATR744',
                        'Last To Win Consecutive Majors': 'ATR745',
                        'Last To Win 3 Consecutive Majors': 'ATR746',
                        'Last To Win 4 Consecutive Majors': 'ATR747',
                        'Last To Earn 1st PGA Tour Win at a Major': 'ATR748',
                        # Playoff Records
                        'Longest Sudden Death Playoff': 'ATR765',
                        'Most Players in a Sudden Death Playoff': 'ATR87',
                        'Most Playoff Appearances in a Season': 'ATR766',
                        'Most Playoffs in a Season': 'ATR88',
                        'Tournament Playoff Records': 'ATR768',
                        # Playoffs: The Last Time
                        'Last To Win Playoff in Consecutive Weeks': 'ATR769',
                        'Last To Win Playoff in Consecutive Starts': 'ATR770',
                        'Last To Lose Playoff in Consecutive Tournaments': 'ATR771',
                        'Last To Lose Playoff in Consecutive Seasons in Same Tournament': 'ATR772',
                        'Last To Earn 1st 3 Wins in Playoffs': 'ATR773',
                        'Last To Lose 3 Playoffs in a Season': 'ATR774',
                        'Last To Win Playoff With an Eagle': 'ATR775',
                        'Last To Win Playoff With a Bogey': 'ATR776',
                        'Last To Win Playoff With a Double Bogey': 'ATR777',
                        'Last 3 Hole Playoff': 'ATR778',
                        'Last 3 Hole Aggregate Playoff': 'ATR779',
                        'Last 4 Hole Playoff': 'ATR780',
                        'Last 4 Hole Aggregate Playoff': 'ATR781',
                        'Last 5 Hole Playoff': 'ATR782',
                        'Last 6 Hole Playoff': 'ATR783',
                        'Last 7 Hole Playoff': 'ATR784',
                        'Last 8 Hole Playoff': 'ATR785',
                        'Last Time 3 Consecutive, Multi-Hole Playoffs': 'ATR787',
                        'Last Time 4 Consecutive Playoffs': 'ATR788',
                        'Last Time 18 Hole Aggregate Playoff': 'ATR789',
                        'Last 18+ Hole Playoff': 'ATR790',
                        'Last 36 Hole Aggregate Playoff': 'ATR792',
                        'Last 54 Hole Aggregate Playoff': 'ATR793',
                        'Last 72 Hole Aggregate Playoff': 'ATR794',
                        'Last 4-Man Playoff': 'ATR795',
                        'Last 5-Man Playoff': 'ATR796',
                        'Last 6-Man Playoff': 'ATR797',
                        # Age-Related Records
                        'Youngest To Play': 'ATR101',
                        'Oldest To Play': 'ATR103',
                        # Leads
                        'Most Leads Entering Final Round Converted To a Win': 'ATR752',
                        'Largest Lead With 18 Holes To Play': 'ATR66',
                        'Largest Lead Lost With 18 Holes To Play': 'ATR163',
                        # Leads: The Last Time
                        'Last Amateur To Lead After Any Round': 'ATR753',
                        'Last Amateur To Play in the Final Group of the Final Round': 'ATR754',
                        'Last Player To Hold Lead/Co-Lead in 1st Round As Professional': 'ATR755',
                        'Last Player To Hold 1st Round Lead/Co-Lead and Miss the Cut': 'ATR756',
                        'Last Leader/Co-Leader After Any Round To Withdraw': 'ATR757',
                        # Cuts
                        'Most Consecutive Cuts Made': 'ATR95',
                        'Most Career Cuts Made': 'ATR96',
                        # Cuts: Age
                        'Youngest To Make Cut': 'ATR102',
                        'Oldest To Make Cut': 'ATR104',
                        # Cuts: The Last Time
                        'Last Father/Son To Make the Cut in the Same Tournament': 'ATR764',
                        # Holes-In-One
                        'All Holes-In-One': 'ATR801',
                        'Seasons With Most Holes-In-One': 'ATR800',
                        'Most Holes-In-One': 'ATR799',
                        # Holes-In-One: The Last Time
                        'Last Time 4 Holes-In-One on Same Hole on Same Day': 'ATR803',
                        'Last To Make a Hole-In-One on the 1st Hole of a Round': 'ATR804',
                        'Last Time 3 Holes-In-One in a Round': 'ATR805',
                        'Last To Make a Hole-In-One and Win': 'ATR806',
                        'Last Time 8 Holes-In-One in a Tournament': 'ATR807',
                        'Last To Make 2 Holes-In-One in a Round': 'ATR92',
                        'Last To Make 2 Holes-In-One in a Tournament': 'ATR93',
                        'Last To Make Hole-In-One on a Par 4': 'ATR94',
                        'Last To Make a Hole-In-One in 1st Professional Start': 'ATR896',
                        'Last Amateur To Record Hole-In-One': 'ATR808',
                        # Money: Money Won
                        'Most Official Money Earned in a Single Season': 'ATR846',
                        'Most Official Money Earned By a Rookie': 'ATR112',
                        'Most Official Money Earned in a Single Season Without a Win': 'ATR116',
                        'Youngest To Earn >$1 Million in a Single Season': 'ATR847',
                        'Biggest One Season Gains in Official Money': 'ATR850',
                        # Money: Money List
                        'Season-By-Season Official Money Leaders': 'ATR851',
                        'Most Seasons Finishing Number 1 on Official Money List': 'ATR113',
                        'Most Seasons Finishing in Top 10 on Official Money List': 'ATR115',
                        'Most Consecutive Seasons Finishing in Top 10 on Official Money List': 'ATR852',
                        'Most Consecutive Seasons Finishing in Top 125 on Official Money List': 'ATR853',
                        'Largest Margin Between Number 1 and Number 2 on Official Money List': 'ATR854',
                        # Money: Growth of Purses
                        'Growth of Purses': 'ATR856',
                        # Official World Golf Ranking
                        'Most Weeks at Number 1': 'ATR858',
                        'Longest Streak at Number 1': 'ATR857',
                        'Number 1 Timeline': 'ATR1008',
                        # Firsts
                        'First African American To Play': 'ATR859',
                        'First African American To Win': 'ATR860',
                        'First African American To Play Sponsored Tournament': 'ATR1007',
                        'Women To Play': 'ATR861',
                        # Last Time - Weather and Tournament Finishes
                        'Last Monday Finish': 'ATR862',
                        'Last Tuesday Finish': 'ATR863',
                        'Last 54 Hole Tournament': 'ATR864',
                        'Last 36 Hole Tournament': 'ATR865',
                        'Last 36 Hole Final Day': 'ATR866',
                        'Last Cut Made After 18 Holes': 'ATR868',
                        'Last Cut Made Closest To 60': 'ATR869',
                        'Last Time a Tournament Had Consecutive Monday Finishes': 'ATR873',
                        'Last Time Back-To-Back Tournaments Had Monday Finishes': 'ATR874',
                        'Last Time 3 Consecutive Tournaments Had Monday Finishes': 'ATR875',
                        'Last Time a Round Restarted': 'ATR876',
                        'Last Time Players Were Not Re-Grouped Between 3rd and Final Rounds': 'ATR877',
                        'Last Round Suspended By Wind': 'ATR882',
                        'Last Round Suspended By Fog': 'ATR883',
                        'Last Round Suspended By Hail': 'ATR884',
                        'Last Round Suspended By Frost': 'ATR885',
                        'Last Time It Snowed During a Tournament': 'ATR878',
                        'Last Time a Tournament Was Suspended and Continued Later in the Season': 'ATR880',
                        'Last Time a Tournament Moved to Later in the Season': 'ATR889',
                        'Last Time a Tournament Was Cancelled and Not Rescheduled': 'ATR879',
                        'Last Tournament Cancelled For Reasons Other Than Weather': 'ATR887',
                        'Last Tournament Spectators Were Not Allowed To Attend For At Least 1 Day': 'ATR1013'
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

####### Use the Following Functions for scraping data from pgatour.com ######
# import statements (comment out when not using)
from bs4 import BeautifulSoup
import requests
import time
import json

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