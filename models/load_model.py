# models/load_model.py

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

TokenizerType = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]

def load_model(
    # Updated to use the lightweight SmolLM2 model by default
    model_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct",
    model_type: Literal["causal", "seq2seq"] = "causal",
) -> Tuple[Optional[PreTrainedModel], Optional[TokenizerType]]:
    """
    Load a Hugging Face model and tokenizer, optimized for CUDA.

    Args:
        model_name (str): Hugging Face model ID.
        model_type (str): 'causal' or 'seq2seq'.

    Returns:
        Tuple of (model, tokenizer), or (None, None) if token is missing.
    """
    hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
    if not hf_token:
        print("⚠️ HUGGINGFACE_HUB_TOKEN is not set in the environment.")
        # Allow loading public models without a token
        print("Proceeding without a token for public models.")

    # Prioritize CUDA if available, otherwise use CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"✅ Using device: {device}")

    # Use bfloat16 for better performance on modern GPUs, otherwise auto
    torch_dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else "auto"

    try:
        tokenizer: TokenizerType = AutoTokenizer.from_pretrained(
            model_name,
            token=hf_token,
            cache_dir="/tmp/huggingface_cache",
        )

        model_class = AutoModelForCausalLM if model_type == "causal" else AutoModelForSeq2SeqLM
        
        model: PreTrainedModel = model_class.from_pretrained(
            model_name,
            token=hf_token,
            torch_dtype=torch_dtype,
            device_map=device,  # Pin the model to the selected device
            cache_dir="/tmp/huggingface_cache",
        )

        print(f"✅ Loaded {model_type.upper()} model '{model_name}' on {model.device}.")
        return model, tokenizer

    except Exception as e:
        print(f"🚫 Error loading model: {e}")
        return None, None

# Example usage
if __name__ == "__main__":
    print("--- Loading Causal LM (SmolLM2) ---")
    model, tokenizer = load_model(model_type="causal")
    if model and tokenizer:
        print(f"Model: {model.__class__.__name__}")
        print(f"Tokenizer: {tokenizer.__class__.__name__}")
