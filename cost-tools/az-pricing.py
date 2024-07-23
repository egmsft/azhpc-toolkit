#!/usr/bin/env python3
import json
import argparse
import requests
from tabulate import tabulate

api_url = "https://prices.azure.com/api/retail/prices"

# generate the query string for the rest API request
# sample of expected query string included below in parameter list:  
# response = requests.get(api_url, params={'$filter': "armRegionName eq 'southcentralus' and armSkuName eq 'Standard_NP20s' and contains(meterName, 'Spot')"}) 
def generate_query(location, sku, pricing_type):
    #query = "armRegionName eq '{}' and serviceName eq 'Virtual Machines'".format(location) -- query for debugging
    query = "armRegionName eq '{}' and armSkuName eq '{}' and priceType eq 'Consumption'".format(location, sku)
    if pricing_type:
        if pricing_type != "Standard":
            query = "{} and contains(meterName, '{}')".format(query, pricing_type)
        else:
            query = "{} and contains(meterName, 'Spot') eq false and contains(meterName, 'Low') eq false".format(query)
    
    return query   


def build_pricing_table(json_data, table_data):
    for item in json_data['Items']:
        meter = item['meterName']
        if('Low' not in meter and 'Spot' not in meter):
            meter = 'Standard'
        table_data.append([item['armSkuName'], item['retailPrice'], item['unitOfMeasure'], item['armRegionName'], meter, item['productName']])

def print_pricing(table_data):
    print(tabulate(table_data, headers='firstrow', tablefmt='psql'))

def main():
    parser = argparse.ArgumentParser(description='Get Azure pricing information')
    parser.add_argument('--location', '-l', help='Azure region', required=True)
    parser.add_argument('--sku', '-s', help='Azure SKU', required=True)
    parser.add_argument('--pricing-type', '-p', help='Azure pricing type', required=False, choices=['Low', 'Spot', 'Standard'])
    args = parser.parse_args()

    table_data = []
    table_data.append(['SKU', 'Retail Price', 'Rate', 'Region', 'Pricing Type', 'Product Name'])

    query = generate_query(args.location, args.sku, args.pricing_type)
    response = requests.get(api_url, params={'$filter': query})
    json_data = json.loads(response.text)
    
    if(not json_data['Items']):
        print("No pricing data found for the specified SKU and location. Please update the sku type or location name and try again.")
        exit(1)

    build_pricing_table(json_data, table_data) 
    nextPage = json_data['NextPageLink']

    while(nextPage):
        response = requests.get(nextPage)
        json_data = json.loads(response.text)
        nextPage = json_data['NextPageLink']
        build_pricing_table(json_data, table_data)

    print_pricing(table_data)
    

if __name__ == "__main__":
    main()