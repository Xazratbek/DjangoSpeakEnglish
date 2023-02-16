from django.shortcuts import render
import requests

def home(request):
    return render(request,'home.html')

def getDefinitions(request):
    app_id = "1d9bd8a2"
    app_key = "a5da10a47ddca7828f157a7c3f4d92e4"
    language = "en-gb"

    word_id = request.GET.get('q','')
    word_id = word_id.strip()
    word_id = word_id.lower()
    if word_id != '':
        url = 'https://od-api.oxforddictionaries.com/api/v2/entries/'  + language + '/'  + word_id.lower()
        r = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
        print(r.status_code)
        res = r.json()

        if 'error' in res.values():
            return render(request,'error_page.html')

        else:
            res = r.json()
            output = {}
            senses = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
            definitions = []
            for sense in senses:
                definitions.append(f" {sense['definitions'][0]}, ")

            output['definitions'] = "\n".join(definitions)

            if res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0].get('audioFile'):
                output['audio'] = res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']

            output['word_id'] = word_id
            context = {
                'result' : output
            }
            return render(request,'home.html',context)

    else:
        output = {}
        output['word_id'] = "None"
        output['definitions'] = "None"
        output['audio'] = "None"
        context = {
            'result' : output
        }
        return render(request,'home.html',context)