# build docs
pdoc --html --force --output-dir docs api
#locally host docs
pdoc --http : api