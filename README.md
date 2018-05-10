# PARticular
A machine learning approach to finding a realistic par (starting with disc golf)


## Dev notes:
To get the data set on yourself, first download the csv version of your scorecards on uDisc.
Then feed that script into the command `csplit --digits=2 --quiet --prefix=ben_dg_csv ~/Downloads/Telegram\ Desktop/udisc-csv-1525834822921.csv "/PlayerName/" "{*}"`
