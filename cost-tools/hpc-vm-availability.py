#!/usr/bin/env python3
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import AzureCliCredential
from azure.mgmt.subscription import SubscriptionClient
import json
import argparse
import requests
from tabulate import tabulate
import multiprocessing

api_url = "https://prices.azure.com/api/retail/prices"

def generate_query(location, sku, pricing_type):
    #query = "armRegionName eq '{}' and serviceName eq 'Virtual Machines'".format(location) -- query for debugging
    query = "armRegionName eq '{}' and armSkuName eq '{}' and priceType eq 'Consumption' and contains(productName, 'Windows') eq false".format(location, sku)
    if pricing_type:
        if pricing_type != "Standard":
            query = "{} and contains(meterName, '{}') and contains(productName, 'Windows') eq false".format(query, pricing_type)
        else:
            query = "{} and contains(meterName, 'Spot') eq false and contains(meterName, 'Low') eq false and contains(productName, 'Windows') eq false".format(query)
    
    return query

def build_pricing_table(json_data, table_data, sku):
    for item in json_data['Items']:
        meter = item['meterName']
        if('Low' not in meter and 'Spot' not in meter):
            meter = 'Standard'
        table_data.append([item['armSkuName'], item['retailPrice'], item['unitOfMeasure'], item['armRegionName'], meter, 
                           sku.number_of_cores, sku.memory_in_mb/1024, sku.max_data_disk_count])
   

def get_hpc_vm_skus(region, credential, subscription, families):

    if not families:
        families = ['N', 'H']
    
    # Create a ComputeManagementClient object
    compute_client = ComputeManagementClient(credential, subscription_id=subscription)

    # List the available virtual machine sizes in the specified region
    vm_sizes = compute_client.virtual_machine_sizes.list(location=region)
    return [sku for sku in vm_sizes if any(series.upper() in sku.name for series in families)]
    #hpc_skus = []
    # Iterate over the virtual machine sizes and print their names
    #for vm_size in vm_sizes:
        # if condition to check if the name of the vm_size has an N or H in it

    #    if 'N' in vm_size.name or 'H' in vm_size.name:
    #        hpc_skus.append(vm_size)

    #return hpc_skus 

def print_pricing(table_data):
    print(tabulate(table_data, headers='firstrow', tablefmt='psql'))

def get_pricing(sku, region):
    table_data = []
    query = generate_query(region, sku.name, "Standard")
    response = requests.get(api_url, params={'$filter': query})
    json_data = json.loads(response.text)
    build_pricing_table(json_data, table_data, sku)
    nextPage = json_data['NextPageLink']

    while(nextPage):
            response = requests.get(nextPage)
            json_data = json.loads(response.text)
            nextPage = json_data['NextPageLink']
            build_pricing_table(json_data, table_data)
    return table_data


def print_regional_skus(region, credential, subscription, families, threads): 
    table_data = []
    table_data.append(['SKU', 'Retail Price', 'Rate', 'Region', 'Pricing Type', 'Core Count', 'Memory (GB)', 'Max Data Disk Count'])
    
    regional_hpc_skus = get_hpc_vm_skus(region, credential, subscription.subscription_id, families)
    tasks = [(sku, region) for sku in regional_hpc_skus]

    pool = multiprocessing.Pool(processes=threads)
    rows = pool.starmap(get_pricing, tasks)
    pool.close()

    for row in rows:
        table_data.extend(row)    
    print_pricing(table_data)   


# create a main function that gets the azure credential
def main():
    parser = argparse.ArgumentParser(description='Get Azure VM availability and pricing information for a given region')
    parser.add_argument('--location', '-l', help='Azure region', required=True)
    parser.add_argument('--families', '-f', nargs='+', help='Azure SKU Families Filter H for H-series, N for N-series', required=False)
    parser.add_argument('--threads', '-t', type=int, help='Number of threads to use', required=False)


    args = parser.parse_args()

    # Acquire a credential object
    credential = DefaultAzureCredential() #AzureCliCredential() #DefaultAzureCredential()
    sub_client = SubscriptionClient(credential)
    subs = sub_client.subscriptions.list()
    
    #get the subscription id of the first subscription
    firstSub = next(subs)

    threads = 16
    if args.threads:
        threads = args.threads
        

    print_regional_skus(args.location, credential, firstSub, args.families, threads)

# invoke the main function
if __name__ == "__main__":
    main()


