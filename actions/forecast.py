from actions import wit

def get_forecast(request):
    print('--- get_forecast() called ---')
    context = request['context']
    entities = request['entities']

    if context:
        print('context : ', context)
    if entities:
        print('entities : ', entities)

    loc = wit.first_entity_value(entities, 'location')
    if loc:
        context['forecast'] = 'sunny'
        if context.get('missingLocation') is not None:
            del context['missingLocation']
    else:
        context['missingLocation'] = True
        if context.get('forecast') is not None:
            del context['forecast']

    return context