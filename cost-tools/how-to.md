# Cost Tools
These utilities include the following scripts: 
- `az-pricing.py` - to query the [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices) for the cost of a SKU of interest in a region of interest
- `hpc-vm-availability.py` - to query the availability and cost of VMs in a region of interest through the use of the Azure Python SDK and the Azure Retail Prices API 

## Installation 
1.  If you don't already have it, [install Python](https://www.python.org/downloads/) and the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

2. [Sign into Azure with the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli) (required for `hpc-vm-availability.py`)

3.  General recommendation for Python development is to use a Virtual Environment.
    For more information, see https://docs.python.org/3/tutorial/venv.html
    
    Install and initialize the virtual environment with the "venv" module on Python 3 (you must install [virtualenv](https://pypi.python.org/pypi/virtualenv) for Python 2.7):
    ```
    python -m venv mytestenv # Might be "python3" or "py -3.6" depending on your Python installation
    cd mytestenv
    source bin/activate      # Linux shell (Bash, ZSH, etc.) only
    ```
### Quickstart
1.  Clone the repository.

    ```
    git clone https://github.com/egmsft/azhpc-toolkit.git
    ```

2.  Install the dependencies using pip or pip3.

    ```
    cd azhpc-toolkit/cost-tools
    pip install -r requirements.txt
    ```
## Demo hpc-vm-availability.py 
`hpc-vm-availability.py`is designed to retrieve a list of available VM Sizes in a given region. It also queries the Retail Prices API to obtain the PAYGO pricing for the list of SKUs that is generated assuming that a Linux OS is used. Note, this tool is designed to run with multiple threads to speed-up the time it takes to query the Prices API and build the output. The output of this script is similar to what you would get if you ran the following Azure CLI command `az vm list-sizes --location "eastus"`. Note that the default behavior of this tool only shows HPC+AI SKUs (HB, HC, HX, NP, NC, ND, NG, and NV), but there is an option to modify the filter if one is also interested in querying for other SKU types:

The run the appliation you simply do the following: 
```
./hpc-vm-availability.py -l <region>
```
Sample output: 
```
./hpc-vm-availability.py -l eastus2
+---------------------------+----------------+--------+----------+----------------+--------------+---------------+-----------------------+
| SKU                       |   Retail Price | Rate   | Region   | Pricing Type   |   Core Count |   Memory (GB) |   Max Data Disk Count |
|---------------------------+----------------+--------+----------+----------------+--------------+---------------+-----------------------|
| Standard_NV6ads_A10_v5    |          0.454 | 1 Hour | eastus2  | Standard       |            6 |            55 |                     4 |
| Standard_NV12ads_A10_v5   |          0.908 | 1 Hour | eastus2  | Standard       |           12 |           110 |                     8 |
| Standard_NV18ads_A10_v5   |          1.6   | 1 Hour | eastus2  | Standard       |           18 |           220 |                    16 |
| Standard_NV36adms_A10_v5  |          4.52  | 1 Hour | eastus2  | Standard       |           36 |           880 |                    32 |
| Standard_NV36ads_A10_v5   |          3.2   | 1 Hour | eastus2  | Standard       |           36 |           440 |                    32 |
| Standard_NV72ads_A10_v5   |          6.52  | 1 Hour | eastus2  | Standard       |           72 |           880 |                    32 |
| Standard_NV12s_v3         |          1.14  | 1 Hour | eastus2  | Standard       |           12 |           112 |                    12 |
| Standard_NV24s_v3         |          2.28  | 1 Hour | eastus2  | Standard       |           24 |           224 |                    24 |
| Standard_NV48s_v3         |          4.56  | 1 Hour | eastus2  | Standard       |           48 |           448 |                    32 |
| Standard_NG8ads_V620_v1   |          0.908 | 1 Hour | eastus2  | Standard       |            8 |            16 |                     8 |
| Standard_NG16ads_V620_v1  |          1.815 | 1 Hour | eastus2  | Standard       |           16 |            32 |                    16 |
| Standard_NG32ads_V620_v1  |          3.63  | 1 Hour | eastus2  | Standard       |           32 |            64 |                    32 |
| Standard_NC4as_T4_v3      |          0.526 | 1 Hour | eastus2  | Standard       |            4 |            28 |                     8 |
| Standard_NC8as_T4_v3      |          0.752 | 1 Hour | eastus2  | Standard       |            8 |            56 |                    16 |
| Standard_NC16as_T4_v3     |          1.204 | 1 Hour | eastus2  | Standard       |           16 |           110 |                    32 |
| Standard_NC64as_T4_v3     |          4.352 | 1 Hour | eastus2  | Standard       |           64 |           440 |                    32 |
| Standard_NV4as_v4         |          0.233 | 1 Hour | eastus2  | Standard       |            4 |            14 |                     8 |
| Standard_NV8as_v4         |          0.466 | 1 Hour | eastus2  | Standard       |            8 |            28 |                    16 |
| Standard_NV16as_v4        |          0.932 | 1 Hour | eastus2  | Standard       |           16 |            56 |                    32 |
| Standard_NV32as_v4        |          1.864 | 1 Hour | eastus2  | Standard       |           32 |           112 |                    32 |
| Standard_NC6s_v3          |          3.06  | 1 Hour | eastus2  | Standard       |            6 |           112 |                    12 |
| Standard_NC12s_v3         |          6.12  | 1 Hour | eastus2  | Standard       |           12 |           224 |                    24 |
| Standard_NC24rs_v3        |         13.464 | 1 Hour | eastus2  | Standard       |           24 |           448 |                    32 |
| Standard_NC24s_v3         |         12.24  | 1 Hour | eastus2  | Standard       |           24 |           448 |                    32 |
| Standard_NC40ads_H100_v5  |          6.98  | 1 Hour | eastus2  | Standard       |           40 |           320 |                     8 |
| Standard_NC80adis_H100_v5 |         13.96  | 1 Hour | eastus2  | Standard       |           80 |           640 |                    16 |
| Standard_NC24ads_A100_v4  |          3.673 | 1 Hour | eastus2  | Standard       |           24 |           220 |                     8 |
| Standard_NC48ads_A100_v4  |          7.346 | 1 Hour | eastus2  | Standard       |           48 |           440 |                    16 |
| Standard_NC96ads_A100_v4  |         14.692 | 1 Hour | eastus2  | Standard       |           96 |           880 |                    32 |
| Standard_ND96amsr_A100_v4 |         32.77  | 1 Hour | eastus2  | Standard       |           96 |          1800 |                    16 |
| Standard_ND96isr_H100_v5  |         98.32  | 1 Hour | eastus2  | Standard       |           96 |          1900 |                    16 |
+---------------------------+----------------+--------+----------+----------------+--------------+---------------+-----------------------+
```

You can filter for specific SKU families based on the first 2 characters that identify the families (e.g., NC just for NC-family, FX just for FX family, H for all HC and HB-family)
```
./hpc-vm-availability.py -l <region> -f <list of SKU families separated by spaces>
```
Sample output: 
```
./hpc-vm-availability.py -l westeurope -f FX NC H
+---------------------------+----------------+--------+------------+----------------+--------------+---------------+-----------------------+
| SKU                       |   Retail Price | Rate   | Region     | Pricing Type   |   Core Count |   Memory (GB) |   Max Data Disk Count |
|---------------------------+----------------+--------+------------+----------------+--------------+---------------+-----------------------|
| Standard_HB120-16rs_v2    |          4.68  | 1 Hour | westeurope | Standard       |          120 |           456 |                    32 |
| Standard_HB120-32rs_v2    |          4.68  | 1 Hour | westeurope | Standard       |          120 |           456 |                    32 |
| Standard_HB120-64rs_v2    |          4.68  | 1 Hour | westeurope | Standard       |          120 |           456 |                    32 |
| Standard_HB120-96rs_v2    |          4.68  | 1 Hour | westeurope | Standard       |          120 |           456 |                    32 |
| Standard_HB120rs_v2       |          4.68  | 1 Hour | westeurope | Standard       |          120 |           456 |                    32 |
| Standard_NC6s_v3          |          3.823 | 1 Hour | westeurope | Standard       |            6 |           112 |                    12 |
| Standard_NC12s_v3         |          7.646 | 1 Hour | westeurope | Standard       |           12 |           224 |                    24 |
| Standard_NC24rs_v3        |         16.821 | 1 Hour | westeurope | Standard       |           24 |           448 |                    32 |
| Standard_NC24s_v3         |         15.292 | 1 Hour | westeurope | Standard       |           24 |           448 |                    32 |
| Standard_HB60-15rs        |          2.964 | 1 Hour | westeurope | Standard       |           15 |           228 |                     4 |
| Standard_HB60-30rs        |          2.964 | 1 Hour | westeurope | Standard       |           30 |           228 |                     4 |
| Standard_HB60-45rs        |          2.964 | 1 Hour | westeurope | Standard       |           45 |           228 |                     4 |
| Standard_HB60rs           |          2.964 | 1 Hour | westeurope | Standard       |           60 |           228 |                     4 |
| Standard_HB120-16rs_v3    |          4.68  | 1 Hour | westeurope | Standard       |          120 |           456 |                    32 |
| Standard_HB120-32rs_v3    |          4.68  | 1 Hour | westeurope | Standard       |          120 |           456 |                    32 |
| Standard_HB120-64rs_v3    |          4.68  | 1 Hour | westeurope | Standard       |          120 |           456 |                    32 |
| Standard_HB120-96rs_v3    |          4.68  | 1 Hour | westeurope | Standard       |          120 |           456 |                    32 |
| Standard_HB120rs_v3       |          4.68  | 1 Hour | westeurope | Standard       |          120 |           456 |                    32 |
| Standard_NC40ads_H100_v5  |          9.08  | 1 Hour | westeurope | Standard       |           40 |           320 |                     8 |
| Standard_NC80adis_H100_v5 |         18.16  | 1 Hour | westeurope | Standard       |           80 |           640 |                    16 |
| Standard_ND96isr_H100_v5  |        127.816 | 1 Hour | westeurope | Standard       |           96 |          1900 |                    16 |
| Standard_NC4as_T4_v3      |          0.658 | 1 Hour | westeurope | Standard       |            4 |            28 |                     8 |
| Standard_NC8as_T4_v3      |          0.94  | 1 Hour | westeurope | Standard       |            8 |            56 |                    16 |
| Standard_NC16as_T4_v3     |          1.505 | 1 Hour | westeurope | Standard       |           16 |           110 |                    32 |
| Standard_NC64as_T4_v3     |          5.44  | 1 Hour | westeurope | Standard       |           64 |           440 |                    32 |
| Standard_NC24ads_A100_v4  |          4.775 | 1 Hour | westeurope | Standard       |           24 |           220 |                     8 |
| Standard_NC48ads_A100_v4  |          9.55  | 1 Hour | westeurope | Standard       |           48 |           440 |                    16 |
| Standard_NC96ads_A100_v4  |         19.1   | 1 Hour | westeurope | Standard       |           96 |           880 |                    32 |
| Standard_HC44-16rs        |          4.118 | 1 Hour | westeurope | Standard       |           16 |           352 |                     4 |
| Standard_HC44-32rs        |          4.118 | 1 Hour | westeurope | Standard       |           32 |           352 |                     4 |
| Standard_HC44rs           |          4.118 | 1 Hour | westeurope | Standard       |           44 |           352 |                     4 |
| Standard_FX4mds           |          0.45  | 1 Hour | westeurope | Standard       |            4 |            84 |                     8 |
| Standard_FX12mds          |          1.35  | 1 Hour | westeurope | Standard       |           12 |           252 |                    24 |
| Standard_FX24mds          |          2.7   | 1 Hour | westeurope | Standard       |           24 |           504 |                    32 |
| Standard_FX36mds          |          4.05  | 1 Hour | westeurope | Standard       |           36 |           756 |                    32 |
| Standard_FX48mds          |          5.4   | 1 Hour | westeurope | Standard       |           48 |          1008 |                    32 |
+---------------------------+----------------+--------+------------+----------------+--------------+---------------+-----------------------+
```

You can also increase the number of threads being used by the application to make it faster. By default it uses 16 threads and usually takes about 3-5 seconds to provide a result. 
```
python hpc-vm-availability.py -l <region> -t <number of threads> 
```
Sample output: 
```
 time ./hpc-vm-availability.py -l eastus
+---------------------------+----------------+--------+----------+----------------+--------------+---------------+-----------------------+
| SKU                       |   Retail Price | Rate   | Region   | Pricing Type   |   Core Count |   Memory (GB) |   Max Data Disk Count |
|---------------------------+----------------+--------+----------+----------------+--------------+---------------+-----------------------|
| Standard_NC4as_T4_v3      |          0.526 | 1 Hour | eastus   | Standard       |            4 |            28 |                     8 |
| Standard_NC8as_T4_v3      |          0.752 | 1 Hour | eastus   | Standard       |            8 |            56 |                    16 |
| Standard_NC16as_T4_v3     |          1.204 | 1 Hour | eastus   | Standard       |           16 |           110 |                    32 |
| Standard_NC64as_T4_v3     |          4.352 | 1 Hour | eastus   | Standard       |           64 |           440 |                    32 |
...
| Standard_ND96asr_v4       |         27.197 | 1 Hour | eastus   | Standard       |           96 |           900 |                    16 |
| Standard_NC40ads_H100_v5  |          6.98  | 1 Hour | eastus   | Standard       |           40 |           320 |                     8 |
| Standard_NC80adis_H100_v5 |         13.96  | 1 Hour | eastus   | Standard       |           80 |           640 |                    16 |
+---------------------------+----------------+--------+----------+----------------+--------------+---------------+-----------------------+

real    0m5.178s
user    0m1.563s
sys     0m0.428s

time ./hpc-vm-availability.py -l eastus -t 32
+---------------------------+----------------+--------+----------+----------------+--------------+---------------+-----------------------+
| SKU                       |   Retail Price | Rate   | Region   | Pricing Type   |   Core Count |   Memory (GB) |   Max Data Disk Count |
|---------------------------+----------------+--------+----------+----------------+--------------+---------------+-----------------------|
| Standard_NC4as_T4_v3      |          0.526 | 1 Hour | eastus   | Standard       |            4 |            28 |                     8 |
| Standard_NC8as_T4_v3      |          0.752 | 1 Hour | eastus   | Standard       |            8 |            56 |                    16 |
| Standard_NC16as_T4_v3     |          1.204 | 1 Hour | eastus   | Standard       |           16 |           110 |                    32 |
| Standard_NC64as_T4_v3     |          4.352 | 1 Hour | eastus   | Standard       |           64 |           440 |                    32 |
...
| Standard_ND96asr_v4       |         27.197 | 1 Hour | eastus   | Standard       |           96 |           900 |                    16 |
| Standard_NC40ads_H100_v5  |          6.98  | 1 Hour | eastus   | Standard       |           40 |           320 |                     8 |
| Standard_NC80adis_H100_v5 |         13.96  | 1 Hour | eastus   | Standard       |           80 |           640 |                    16 |
+---------------------------+----------------+--------+----------+----------------+--------------+---------------+-----------------------+

real    0m3.790s
user    0m1.423s
sys     0m0.787s

```
## Demo az-prycing.py
`az-pricing.py`is designed to retrieve pricing information for a given SKU in a given region. It lists the PAYGO (Standard), Spot, and the Low Priority hourly rate of running the SKU in the given region. 

The run the appliation you simply do the following: 
```
./az-pricing.py -l <region> -s SKU
```
Sample output: 
```
./az-pricing.py -s Standard_HB120rs_v3 -l southcentralus 
+---------------------+----------------+--------+----------------+-------------------------+----------------------------------------+
| SKU                 |   Retail Price | Rate   | Region         | Pricing Type            | Product Name                           |
|---------------------+----------------+--------+----------------+-------------------------+----------------------------------------|
| Standard_HB120rs_v3 |          0.948 | 1 Hour | southcentralus | HB120rs_v3 Spot         | Virtual Machines HBrsv3 Series Windows |
| Standard_HB120rs_v3 |          0.396 | 1 Hour | southcentralus | HB120rs_v3 Spot         | Virtual Machines HBrsv3 Series         |
| Standard_HB120rs_v3 |          0.792 | 1 Hour | southcentralus | HB120rs_v3 Low Priority | Virtual Machines HBrsv3 Series         |
| Standard_HB120rs_v3 |          3.792 | 1 Hour | southcentralus | HB120rs_v3 Low Priority | Virtual Machines HBrsv3 Series Windows |
| Standard_HB120rs_v3 |          9.48  | 1 Hour | southcentralus | Standard                | Virtual Machines HBrsv3 Series Windows |
| Standard_HB120rs_v3 |          3.96  | 1 Hour | southcentralus | Standard                | Virtual Machines HBrsv3 Series         |
+---------------------+----------------+--------+----------------+-------------------------+----------------------------------------+
```
## Notes
- All prices shown are in USD
-  


