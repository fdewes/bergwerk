from data import ollama as data
from data import wiki as wikidata 
from service import wiki as service_wiki

def query_llm(textinput):

    response = data.query_llm(textinput)

    return response


def llm_training_data():
    pages = wikidata.get_all_pages_of_category("http://wiki/w", "Content")

    for p in pages:

        en_text = service_wiki.get_page(page=p, language="English").text

        instruction = """
        The following might be an answer to multiple questions. Please hypothesize five to ten questions which could trigger this answer and seperate them with a line break.      
        """

        prompt = instruction + "\n" + en_text 

        r = data.query_llm(prompt)

        print()
        full_page = wikidata.get_entire_page("http://wiki/w", p)
        full_page += "\n= Training Questions =\n" + r['response']

        wikidata.create_or_update_page("http://wiki/w", p, full_page)



