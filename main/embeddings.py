from transformers import AutoTokenizer, AutoModel
from torch import Tensor
import torch.nn.functional as F

tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-base')
model = AutoModel.from_pretrained('intfloat/multilingual-e5-base')


def embedding_engine_helper_function(
    last_hidden_states: Tensor, attention_mask: Tensor
) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)

    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def embedding_engine(input):
    input_text = f"query: {input}"

    batch_dict = tokenizer(
        input_text, max_length=512, padding=True, truncation=True, return_tensors="pt"
    )

    outputs = model(**batch_dict)

    embeddings = embedding_engine_helper_function(
        outputs.last_hidden_state, batch_dict["attention_mask"]
    )

    embeddings = F.normalize(embeddings, p=2, dim=1).detach().numpy()

    return embeddings
