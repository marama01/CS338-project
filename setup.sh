#!/bin/bash

while getopts 'sdlh' opt; do
  case "$opt" in
    s) 
      echo "Setting up sql database"
      mysql -u root -p < sql/setup.sql
      ;;
    d) 
      echo "Deleting testdb database"
      mysql -u root -p < sql/drop_db.sql
      ;;
    l) echo "Loading sample.csv database"
      mysql -u root -p --local-infile < sql/load_sample.sql
      ;;

    h)
      echo "Usage: $(basename $0) [-s] [-d] [-l]"
      exit 1
      ;;
    esac
done
