# Module to interface with AnkiConnect
# The following code has been obtained from github.com/FooSoft/anki-connect
import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

# Own code starts below
def get_learned_cards (deck_name):
    # Field in Anki
    target_field = "Vocabulary-Kanji"

    try:
        print("> Getting Anki cards...")
        card_ids    = invoke("findCards", query=f"deck:\"{deck_name}\" is:review -is:suspended")
        notes       = invoke("cardsInfo", cards=card_ids)

        # Iterate notes, extracting only a specific field
        subjects = []
        print("> Extracting subjects...")
        for note in notes:
            subjects.append(note["fields"][target_field]["value"])

        with open("anki_vocab.txt", "w") as f:
            for subject in subjects:
                f.write(f"{subject}\n")
        
        return subjects

    except Exception as e:
        print(f"OOF: {str(e)}")