# build docs
pdoc --html --force --output-dir docs wsimple/api
#locally host docs
pdoc --http : wsimple/api