#!/bin/bash

rm ../bookshelf.js
for f in $(ls *.js)
do
    echo "Concatenating $f"
    cat $f >> ../bookshelf.js
done

cp ../bookshelf.js ../static/bookshelf.js
