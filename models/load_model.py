import os
from dotenv import load_dotenv
import torch
from typing import Tuple, Optional, Literal, Union, cast
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
)
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast
from transformers.tokenization_utils import PreTrainedTokenizer
from transformers.modeling_utils import PreTrainedModel

# Load environment variables from .env file

load_dotenv()
hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")

TokenizerType = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]

def load_model(
    model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    model_type: Literal["causal", "seq2seq"] = "causal",
) -> Tuple[Optional[PreTrainedModel], Optional[TokenizerType]]:
    """
    Load a Hugging Face model and tokenizer using the HUGGINGFACE_HUB_TOKEN from the environment.

    Args:
        model_name (str): Hugging Face model ID.
        model_type (str): 'causal' or 'seq2seq'.

    Returns:
        Tuple of (model, tokenizer), or (None, None) if token is missing.
    """
    hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
    if not hf_token:
        print("⚠️ HUGGINGFACE_HUB_TOKEN is not set in the environment.")
        return None, None

    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.bfloat16 if device == "cuda" and torch.cuda.is_bf16_supported() else "auto"

    tokenizer: TokenizerType = AutoTokenizer.from_pretrained( # type: ignore
        model_name,
        token=hf_token,
        cache_dir="/tmp",
    )

    if model_type == "causal":
        model: PreTrainedModel = AutoModelForCausalLM.from_pretrained( # type: ignore
            model_name,
            token=hf_token,
            torch_dtype=torch_dtype,
            device_map="auto",
            cache_dir="/tmp",
        )
    elif model_type == "seq2seq":
        model: PreTrainedModel = AutoModelForSeq2SeqLM.from_pretrained( # type: ignore
            model_name,
            token=hf_token,
            torch_dtype=torch_dtype,
            device_map="auto",
            cache_dir="/tmp",
        )
    else:
        raise ValueError(f"Invalid model_type '{model_type}'. Must be 'causal' or 'seq2seq'.")

    print(f"✅ Loaded {model_type.upper()} model '{model_name}' on {cast(PreTrainedModel, model).device}.")
    model = cast(Optional[PreTrainedModel], model) # type: ignore
    tokenizer = cast(Optional[TokenizerType], tokenizer) # type: ignore
    return model, tokenizer

# Example usage
if __name__ == "__main__":
    print("--- Loading Causal LM ---")
    model, tokenizer = load_model(model_type="causal")
    if model and tokenizer:
        print(f"Model: {model.__class__.__name__}")
        print(f"Tokenizer: {tokenizer.__class__.__name__}")
