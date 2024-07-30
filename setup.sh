#!/bin/bash
CONFIG_FILE="config.json"
USERNAME=$(jq -r '.username' "$CONFIG_FILE")
PASSWORD=$(jq -r '.password' "$CONFIG_FILE")

show_menu() {
    echo "Choose an option:"
    echo "1) Set up SQL database"
    echo "2) Delete testdb database"
    echo "3) Load sample.csv database"
    echo "4) Load gen_prod_data.csv database"
    echo "5) Regenerate production data"
    echo "6) Run Flask service"
    echo "7) Exit"
}

handle_choice() {
    case "$1" in
        1) 
            echo
            mysql -u"$USERNAME" -p"$PASSWORD" < sql/setup.sql 
            ;;
        2) 
            echo
            mysql -u"$USERNAME" -p"$PASSWORD" < sql/drop_db.sql 
            ;;
        3) 
            echo
            mysql -u"$USERNAME" -p"$PASSWORD" --local-infile < sql/load_sample.sql 
            ;;
        4) 
            echo
            mysql -u"$USERNAME" -p"$PASSWORD" --local-infile < sql/load_prod_data.sql 
            ;;
        5) 
            while true; do
                read -rp "Enter the amount of data you want to generate (like 10000 or 1000000): " number
                if [[ $number =~ ^[0-9]+$ ]]; then
                    cd prod_data
                    python3 ./gen_prod_data.py "$number"
                    cd ..
                    break
                else
                    echo "Invalid input. Please enter a valid number."
                fi
            done
            echo "Successfully generate production data with number: $number"
            echo
            ;;
        6) 
            echo "Beginning to run Flask service"
            echo
            flask --app backend/app run --debug
            ;;
        7)
            echo "Exiting..."
            echo
            exit 0
            ;;
        *) 
            echo "Invalid option. Please try again."
            echo
            ;;
    esac
}

YELLOW='\033[1;33m'
NC='\033[0m'
echo -e "${YELLOW}HINT:${NC}"
echo -e "${YELLOW}The correct step is setup DB, generate data, import data, run flask service${NC}"
echo

while true; do
    show_menu
    read -rp "Enter your choice: " choice
    handle_choice "$choice"
done
