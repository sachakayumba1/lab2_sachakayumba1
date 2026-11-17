#!/bin/bash

# 1. Archive Directory Check
if [ ! -d "archive" ]; then
    mkdir archive
fi

# 2. Archival Process
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED_FILE="archive/grades_${TIMESTAMP}.csv"

if [ -f "grades.csv" ]; then
    mv grades.csv "$ARCHIVED_FILE"
    # 3. Workspace Reset
    touch grades.csv
    # 4. Logging
    echo "$(date +"%Y-%m-%d %H:%M:%S") | Archived: grades.csv -> $ARCHIVED_FILE" >> organizer.log
else
    echo "Error: grades.csv does not exist."
fi
