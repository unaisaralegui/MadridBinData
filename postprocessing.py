import sys
import requests
import json
import pandas as pd

# Simple script to show the parameters sent to the script, and generate a dummy file

def update_data(existing_data, new_data_path):
    if existing_data is not None:
        max_date = existing_data['fecha'].max()
    else:
        max_date = None
    with open(new_data_path, 'r') as f:
        new_data = json.load(f)
    new_dataf = pd.DataFrame(new_data['papeleras'])
    if max_date is not None:
        new_dataf_filtered = new_dataf.loc[new_dataf['fecha'] > max_date]
    else: 
        new_dataf_filtered = new_dataf
    new_dataf_filtered = new_dataf_filtered.sort_values(by=['fecha'])
    return new_dataf_filtered



if __name__ == "__main__":
    filename = 'data.csv'
    new_data_path = sys.argv[1]
    try:
        existing_data = pd.read_csv(filename)
    except:
        existing_data = None
    new_data = update_data(existing_data=existing_data, new_data_path=new_data_path)
    if new_data is not None:
        print(f"Adding {len(new_data)} new rows")
        if existing_data is not None:
            new_data.to_csv(filename, mode='a', header=False, index=False)
        else:
            new_data.to_csv(filename, index=False)
