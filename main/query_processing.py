from gpt_functions import batch_summarize_text, gpt_final_answer
from document_generator import generate_pdf
from database_analyzer import search_index
from embeddings import embedding_engine

def query_classifier(jurisdiction):

    if jurisdiction == "federal":

        folder = "federal/leyes_federales"

    elif jurisdiction == "state":

        folder = "federal/leyes_estatales"

    elif jurisdiction == "municipal":

        folder = "state/reglamentos_municipales/monterrey"

    else:
        folder = None

    return folder

def process_query(query, jurisdiction):

    folder = query_classifier(query, jurisdiction)

    embedding = embedding_engine(query)

    focused_docs = search_index(embedding, folder)

    summarized_text = batch_summarize_text(query, focused_docs, folder)

    reply = gpt_final_answer(query, summarized_text)

    document_path = generate_pdf(query, reply)

    return reply, document_path