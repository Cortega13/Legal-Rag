from chunks_map import map_indices_to_text_chunks
from concurrent.futures import ThreadPoolExecutor
from rate_limited_api import RateLimitedAPI
import nltk

api = RateLimitedAPI()

def gpt_rate_limited_with_queue(conversation_histories):
    print(f"Length of requests: {len(conversation_histories)}")
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(api.request, ch) for ch in conversation_histories]

        results = []
        for future in futures:
            # This will block until the future is complete
            result = future.result()
            results.append(result)

    return results

def batch_summarize_text(query, docs_list, base_path, max_length=2000, num_docs_=4):
    text_batches = []

    for doc in docs_list[:num_docs_]:
        path_id = doc[0]
        list_of_sections = doc[1]

        text_sections = map_indices_to_text_chunks(path_id, base_path, list_of_sections)
        concatenated_text_sections = " ".join(text_sections)
        sentences = nltk.sent_tokenize(concatenated_text_sections)

        start = 0
        while start < len(sentences):
            end = start
            text_batch = ""
            while (
                end < len(sentences)
                and len(text_batch) + len(sentences[end]) <= max_length
            ):
                text_batch += sentences[end]
                end += 1

            text_batches.append(text_batch)

            start = end

    summaries = gpt_text_summarizer(query, text_batches)

    full_summary = " ".join(summaries)

    return full_summary

def gpt_text_summarizer(query, batch_docs):
    conversation_history = [
        [
            {
                "role": "system",
                "content": "As a legal specialist named Steven, you are required to provide comprehensive responses in English, adhering strictly to the provided instructions. You reply using efficient jargon to minimize the number of words used in your reply, without loss of quality. You prioritize logic in your reply and explain like I'm 5.",
            },
            {
                "role": "user",
                "content": f"Read the following then stay idle by saying 'IDLE'. {docs}",
            },
            {"role": "assistant", "content": "IDLE."},
            {
                "role": "user",
                "content": f"Using the information I provided, extract only information that may be useful in answering the question '{query}'. Reply in a rephrased manner using efficient jargon to minimize the number of words used, without losing any relevant information in the extraction and rephrasing. If the information provided is insufficient for answering the query, only reply with 'null'. Reply in english.",
            },
        ]
        for docs in batch_docs
    ]
    reply = gpt_rate_limited_with_queue(conversation_history)
    return reply

def gpt_final_answer(query, summarized_text):
    conversation_history = [
        [
            {
                "role": "system",
                "content": "As a legal specialist named Steven, you are required to provide comprehensive responses in English, adhering strictly to the provided instructions. You prioritize logic, quality, formatting, and length in your responses. You explain logically and like I'm 14 years old.",
            },
            {
                "role": "user",
                "content": f"Read the following then stay idle by saying 'IDLE'.\n{summarized_text}",
            },
            {"role": "assistant", "content": "IDLE"},
            {
                "role": "user",
                "content": f"Using the information I provided, extract and format all information that may be relevant to the query '{query}', starting with an answer. You may only use the information I gave you. Do not acknowledge that I gave you this information, you will pretend you already knew it. Let's think about this logically and provide good details to support your answer. Reply in english and explain like I'm in 14 years old.",
            },
        ]
    ]
    reply = gpt_rate_limited_with_queue(conversation_history)[0]
    return reply
