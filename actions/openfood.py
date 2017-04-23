from actions import wit
from actions.RequestOpenFood import RequestOpenFood
from actions.RequestOpenFood import ProductBuilder

def getOpenFoodInfo(request):
    print('--- get_openfood() called ---')
    context = request['context']
    entities = request['entities']

    product = wit.first_entity_value(entities, 'product_id')
    if product:

        try:
            res = RequestOpenFood.get_product(barcode=product)
            #res = ProductBuilder.clean_data(res)
            context['info'] = "Found info but can't write it"
            if context.get('missing_id') is not None:
                del context['missing_id']
        except:
            context['info'] = "Can't find this product on the OpenFood database"
    else:
        context['missing_id'] = True
        if context.get('info') is not None:
            del context['info']

    return context