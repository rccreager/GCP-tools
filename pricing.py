from googleapiclient.discovery import build

def get_sku_list(service_name):
    #first build the API service
    api_service = build('cloudbilling', 'v1')

    #now i get all of the SKUs corresponding to a particular service
    # "services/6F81-5844-456A" is the name for compute engine
    sku_list = api_service.services().skus().list(parent=service_name).execute()
    sku_list = sku_list['skus']
    return sku_list

def get_service_list():
    #first build the API service
    api_service = build('cloudbilling', 'v1')

    #now i get all of the services available 
    service_list = api_service.services().list().execute()
    service_list = service_list['services']
    return service_list 

def get_sku_price(sku):
    pricingExpression = sku['pricingInfo'][0]['pricingExpression']
    try:
        tieredRates = pricingExpression['tieredRates'][0]
    except IndexError as error:
        print("Bad tieredRate index. No pricing available.")
        return(0.,'GiBy',0.,'USD')
    unit_price_whole = tieredRates['unitPrice']['units']
    unit_price_nanos = tieredRates['unitPrice']['nanos']
    unit_price_currency = tieredRates['unitPrice']['currencyCode']
    display_quantity = pricingExpression['displayQuantity']
    usage_unit = pricingExpression['usageUnit']
    unit_price = float(unit_price_whole) + float(unit_price_nanos) * 1.0e-9
    return unit_price, unit_price_currency, display_quantity, usage_unit

def calculate_unit_quota(sku, quota):
    unit_price, unit_price_currency, display_quantity, usage_unit = get_sku_price(sku)
    if (display_quantity <= 0 or unit_price <= 0):
        return -1.
    ratio = float(display_quantity) / (unit_price * float(display_quantity)) 
    return quota*ratio

def print_all_sku_prices(service_name, quota=100, on_demand_only=True): 
    sku_list = get_sku_list(service_name) 
    for sku in sku_list:
        #if (service['category']['usageType'] == 'OnDemand' and service['category']['resourceGroup'] == ('CPU' or 'GPU')):
        if (sku['category']['usageType'] == 'OnDemand' or not on_demand_only):
            print(sku['category'])
            print(sku['description'])
            unit_price, unit_price_currency, display_quantity, usage_unit = get_sku_price(sku)
            ratio = calculate_unit_quota(sku, quota)
            value = unit_price * float(display_quantity)
            print("{:6.3f}".format(value) + " " + unit_price_currency + " per " + str(display_quantity) + " " + usage_unit)
            #print(str(unit_price * float(display_quantity)) + " " + unit_price_currency + " per " + str(display_quantity) + " " + usage_unit)
            print("{:6.3f}".format(ratio) + " " + usage_unit + " per " + str(quota) + " " + unit_price_currency)
            print(" ")

def print_all_services():
    service_list = get_service_list()
    for service in service_list:
        print(service['displayName'])



