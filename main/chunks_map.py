import json

def map_search_indices_to_file_identifiers(indices, base_path):
    with open(f"{base_path}/schema_with_indices.json", "r") as infile:
        data = json.load(infile)
    titles_and_positions = []
    for index in indices:
        for item in data:
            if item["start"] <= index <= item["end"]:
                relative_position = index - item["start"]
                titles_and_positions.append([item["path_id"], relative_position])
                break
    return titles_and_positions


def map_indices_to_text_chunks(path_id, base_path, indices):
    text_chunks_json_path = f"{base_path}/pdfs/{path_id}/{path_id}.json"
    with open(text_chunks_json_path) as f:
        all_chunks = json.load(f)

    relevant_chunks = []

    for index in indices:
        relevant_chunks.append(all_chunks[index])

    print(relevant_chunks)
    return relevant_chunks
