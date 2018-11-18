from googleapiclient.discovery import build

#first build the API service
api_service = build('cloudbilling', 'v1')

#now i get all of the SKUs corresponding to a particular service
# "services/6F81-5844-456A" is the name for compute engine
list_services = api_service.services().skus().list(parent="services/6F81-5844-456A").execute()
list_services = list_services['skus'] 

for service in list_services:
    #if (service['category']['usageType'] == 'OnDemand' and service['category']['resourceGroup'] == ('CPU' or 'GPU')):
    if (service['category']['usageType'] == 'OnDemand'):
        print(service['description'])
        pricingExpression = service['pricingInfo'][0]['pricingExpression']
        try:
            tieredRates = pricingExpression['tieredRates'][0]
        except IndexError as error:
            print("bad tieredRate index, no pricing available")
            continue

        unitPriceWhole = tieredRates['unitPrice']['units']
        unitPriceNanos = tieredRates['unitPrice']['nanos']
        unitPriceCurrency = tieredRates['unitPrice']['currencyCode']
        displayQuantity = pricingExpression['displayQuantity']
        usageUnit = pricingExpression['usageUnit']
        unitPrice = float(unitPriceWhole) + float(unitPriceNanos) * 1.0e-9
        
        print(str(unitPrice * float(displayQuantity)) + " " + unitPriceCurrency + " per " + str(displayQuantity) + " " + usageUnit)
