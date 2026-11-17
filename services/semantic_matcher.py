
import os

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "all-MiniLM-L6-v2"
)

MODEL_PATH = os.path.join(MODEL_DIR, "model.onnx")
TOKENIZER_PATH = os.path.join(MODEL_DIR, "tokenizer.json")

MAX_LENGTH = 256
CONTENT_LENGTH = MAX_LENGTH - 2

_tokenizer = None
_session = None


def load_model():

    global _tokenizer, _session

    if _tokenizer is None:
        _tokenizer = Tokenizer.from_file(TOKENIZER_PATH)
        _tokenizer.no_truncation()
        _tokenizer.no_padding()

    if _session is None:
        _session = ort.InferenceSession(
            MODEL_PATH,
            providers=["CPUExecutionProvider"]
        )

    return _tokenizer, _session


def generate_embedding(text):

    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    tokenizer, session = load_model()

    encoded = tokenizer.encode(
        text,
        add_special_tokens=False
    )

    token_ids = encoded.ids

    if not token_ids:
        raise ValueError("No tokens found in input text.")

    cls_id = tokenizer.token_to_id("[CLS]")
    sep_id = tokenizer.token_to_id("[SEP]")
    pad_id = tokenizer.token_to_id("[PAD]")

    if None in (cls_id, sep_id, pad_id):
        raise ValueError("Required tokenizer special tokens are missing.")

    chunks = [
        token_ids[i:i + CONTENT_LENGTH]
        for i in range(0, len(token_ids), CONTENT_LENGTH)
    ]

    input_ids = []
    attention_masks = []
    token_type_ids = []

    for chunk in chunks:

        ids = [cls_id] + chunk + [sep_id]
        padding_length = MAX_LENGTH - len(ids)

        input_ids.append(
            ids + [pad_id] * padding_length
        )

        attention_masks.append(
            [1] * len(ids) + [0] * padding_length
        )

        token_type_ids.append(
            [0] * MAX_LENGTH
        )

    input_ids = np.array(input_ids, dtype=np.int64)
    attention_masks = np.array(attention_masks, dtype=np.int64)
    token_type_ids = np.array(token_type_ids, dtype=np.int64)

    outputs = session.run(
        ["last_hidden_state"],
        {
            "input_ids": input_ids,
            "attention_mask": attention_masks,
            "token_type_ids": token_type_ids
        }
    )

    token_embeddings = outputs[0]

    mask = attention_masks.astype(np.float32)[..., None]

    summed_embeddings = np.sum(
        token_embeddings * mask,
        axis=1
    )

    token_counts = np.maximum(
        np.sum(mask, axis=1),
        1e-9
    )

    chunk_embeddings = summed_embeddings / token_counts

    # Aggregate chunk embeddings using their content-token counts.
    chunk_weights = np.array(
        [len(chunk) for chunk in chunks],
        dtype=np.float32
    )

    sentence_embedding = np.average(
        chunk_embeddings,
        axis=0,
        weights=chunk_weights
    )

    norm = np.linalg.norm(sentence_embedding)

    sentence_embedding = sentence_embedding / max(
        norm,
        1e-12
    )

    return sentence_embedding.astype(np.float32)


def calculate_semantic_similarity(resume_text, job_description):

    resume_embedding = generate_embedding(resume_text)
    job_embedding = generate_embedding(job_description)

    similarity = np.dot(
        resume_embedding,
        job_embedding
    )

    similarity = float(np.clip(similarity, -1.0, 1.0))

    return round(similarity * 100, 2)
