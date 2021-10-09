# handball-rapm
An initial effort to build out regularized adjusted plus-minus in team handball.

## Background
The Men's EHF EURO 2020 Championship was the first handball event I came across that had "Lineup Report" files that easily provide lineup efficencies. Handball is like hockey where there is live subbing during the game so not only is it hard to track yourself, play-by-play usually doesn't include it. Here is an example of one for the [championship game](https://livecache.sportresult.com/node/binaryData/HBL_PROD/HBEC20M/PDF_P65LU.PDF). While these are not exactly machine readable, this provides us with a tremendous starting point to build out at least a first attempt a regularized adjusted plus-minus (RAPM) for a handball tournament/league. While a single tournament, even one of the bigger ones like EUROs might be too small of a sample for RAPM, I figured it would still be a valuable exercise and can help get the ball rolling on handball analytics. So far I've found these reports for both Men's and Women's EURO tournaments going back to 2014. 

## Info
There are three main steps to generating RAPM here:
- Data: Downloading the lineup reports
- Parsing: Parsing them into a usable state
- Calculations: Generating RAPM values

## Next Steps
Ideally this can be used to develop weights for some sort of box plus-minus model. That way we can generate numbers for all games with Match Reports which is almost every other major handball game, but a hurdle there is Match Reports do not disclose minutes played for each player (probably due to live ball subbing). So some sort of possessions played model will probably need to be built out, too.

### [Data](https://github.com/nmjohnson/handball-rapm/tree/main/Data)
The data comes from official lineup report PDF files. I have created batch scripts to automatically pull those down and put them in the [Data](https://github.com/nmjohnson/handball-rapm/tree/main/Data) folder. I have created batch scripts for all of the tournaments I can find that have these type of Lineup Report/Line Analysis files, please let me know if I am missing any!

### [Parsing](https://github.com/nmjohnson/handball-rapm/tree/main/Parsing)
The parser I built, ```handball_lineup_report_parser.py```, takes a folder of lineup report PDF's, parses them for lineup shifts, and outputs them all into one .csv file. You can see the parser and same example output files in the [Parsing](https://github.com/nmjohnson/handball-rapm/tree/main/Parsing) folder. **NOTE:** The PDF parser I built out was not tested on non-2020 tournaments so I can't guarantee it works on the earlier tournaments.

**NOTE:** The lineup reports presents the players without distinguishing between position and includes jersey number as well as full name. Since full names can be anywhere from one single word to four or more words combined my parser has not be exhaustively tested for all potential names, but seems to do a pretty good job at isolating jersey numbers which is what are used going forward in this process. At this point goalies are included in the lineups, although you might want to exclude them, but there is not currently a way to do that other than manually identify all goalie id's, drop them, and reshuffle the 7 columns into 6 columns all with valid player id's.

```handball_lineup_report_parser.py -i <inputdirectory> -o <outputfile>```

### [Calculations](https://github.com/nmjohnson/handball-rapm/tree/main/Calculations)
Once you have a parsed lineup shifts file, you can generate RAPM. To do that, simply feed the input csv file into ```handball_rapm_7v7.py``` or ```handball_rapm_6v6.py``` and dictate where you want the output file to be. This code was modified from  [Kosta Pelechrinis'](https://github.com/kpelechrinis) Ridge APM script located [here](https://sites.pitt.edu/~kpele/ridge_apm.py). I prefer to generate RAPM only for non-goalies and for goals they scored (so excluding goals allowed), but this is up to you. Instead of properly determining a mean per-possession value (like per 100 posssessions in basketball), shifts are weighted by relative length to average shift length. This can also be modified and probably improved as it doesn't give the nubmers proper game context but rather only relative context.

```handball_rapm_6v6.py -i <inputfile> -o <outputfile>```
