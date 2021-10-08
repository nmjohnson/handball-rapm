# handball-rapm
An initial effort to build out regularized adjusted plus-minus in team handball.

## Background
The Men's EHF EURO 2020 Championship was the first handball event I came across that had "Lineup Report" files that easily provide line efficencies. Here is an example of one for the [championship game](https://livecache.sportresult.com/node/binaryData/HBL_PROD/HBEC20M/PDF_P65LU.PDF). While these are not exactly machine readable, this provides us with a tremendous starting point to build out at least a first attempt a regularized adjusted plus-minus (RAPM) for a handball tournament/league. While a single tournament, even one of the bigger ones like EUROs might be too small of a sample for RAPM, I figured it would still be a valuable exercise and can help get the ball rolling on handball analytics.

## Info
There are thre main steps to generating RAPM here:
- Data: Downloading the lineup reports
- Parsing: Parsing them into a usable state
- Calculations: Generating RAPM values

### [Data](https://github.com/nmjohnson/handball-rapm/tree/main/Data)
The data comes from official lineup report PDF files. I have created batch scripts to automatically pull those down and put them in the [Data](https://github.com/nmjohnson/handball-rapm/tree/main/Data) folder.

### [Parsing](https://github.com/nmjohnson/handball-rapm/tree/main/Parsing)
The parser I built, ```handball_lineup_report_parser.py```, takes a folder of lineup report PDF's, parses them for lineup shifts, and outputs them all into one .csv file. You can see the parser and same example output files in the [Parsing](https://github.com/nmjohnson/handball-rapm/tree/main/Parsing) folder. **NOTE:** The lineup reports presents the players without distinguishing between position and includes jersey number as well as full name. Since full names can be anywhere from one single word to four or more words combined my parser has not be exhaustively tested for all potential names, but seems to do a pretty good job at isolated jersey numbers which is what are used going forward. At this point goalies are included in the lineups, although you might want to exclude them, but there is not currently a way to do that other than manually identify all goalie id's, dropping them, and reshuffling the 7 columns into 6 columns all with valid player id's.

### Calculations
