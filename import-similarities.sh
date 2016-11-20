#!/bin/bash
FILES=private/final-dfs/*
for f in $FILES
do
    mongoimport -h localhost:3001 --db meteor --collection similarities \
    --type csv --headerline --file $f
done