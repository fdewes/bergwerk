from data import ollama as data

def query_llm(textinput):

    response = data.query_llm(textinput)

    return response