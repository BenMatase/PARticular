mkdir workspace

# remove extra new lines
sed -i '/^$/d' $1

# remove spaces after `,`
sed -i -e 's/, /,/g' $1 

# split into files
# TODO: this has small issue where if any other text with PlayerName in the csv will break stuff
csplit --digits=2 --quiet --prefix=./workspace/ben_dg_csv $1 "/PlayerName/" "{*}"
