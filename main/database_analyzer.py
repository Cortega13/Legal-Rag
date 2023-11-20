from chunks_map import map_search_indices_to_file_identifiers
from collections import defaultdict
import faiss

def expand_sections(sections, range_=1):
    expanded = set()
    for sec in sections:
        expanded.update(range(max(0, sec - range_), sec + range_ + 1))
    return sorted(list(expanded))

def combine_sections(documents):
    result_dict = defaultdict(list)
    for title, section in documents:
        result_dict[title].append(int(section))

    for title, sections in result_dict.items():
        result_dict[title] = expand_sections(sections)

    result_list = [[title, sections] for title, sections in result_dict.items()]

    return result_list

def search_index(embedding, base_path, k_results_=30):
    index = faiss.read_index(f"{base_path}/{base_path.split('/')[-1]}.index")

    distances, indices = index.search(embedding.reshape(1, -1), k_results_)

    results = map_search_indices_to_file_identifiers(indices[0], base_path)

    results = combine_sections(results)

    print(results)

    return results
