from actions import wit
from openfood import RequestOpenFood
#from openfood.RequestOpenFood import ProductBuilder

def getOpenFoodInfo(request):
    print('--- get_openfood() called ---')
    context = request['context']
    entities = request['entities']

    if context:
        print('context : ', context)
    if entities:
        print('entities : ', entities)



    return context