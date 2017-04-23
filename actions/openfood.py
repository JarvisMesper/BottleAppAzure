from actions import wit
from actions import requestopenfood

def getOpenFoodInfo(request):
    print('--- get_openfood() called ---')
    context = request['context']
    entities = request['entities']

    if context:
        print('context : ', context)
    if entities:
        print('entities : ', entities)



    return context