from typing import Optional
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.pipelines import pipeline # type: ignore
from transformers.pipelines.text_generation import TextGenerationPipeline
from transformers.modeling_utils import PreTrainedModel
from models.load_model import load_model
from transformers.tokenization_utils import PreTrainedTokenizer
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast

# --- Global Setup ---
_model: Optional[PreTrainedModel]
_tokenizer: Optional[PreTrainedTokenizerBase]
_model, _tokenizer = load_model(
    model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    model_type="causal"
    
)

_summarizer_pipeline: Optional[TextGenerationPipeline] = None
if _model is not None and _tokenizer is not None:
    from transformers.tokenization_utils import PreTrainedTokenizer
    from transformers.tokenization_utils_fast import PreTrainedTokenizerFast
    if isinstance(_tokenizer, PreTrainedTokenizer):
        tokenizer_cast = _tokenizer
    elif isinstance(_tokenizer, PreTrainedTokenizerFast): # type: ignore
        tokenizer_cast = _tokenizer
    else:
        raise TypeError("Loaded tokenizer is not a valid PreTrainedTokenizer or PreTrainedTokenizerFast instance.")
    _summarizer_pipeline = pipeline(
        "text-generation",
        model=_model,
        tokenizer=tokenizer_cast,
    )
# --- End Global Setup ---


def summarize_text(text: str) -> str:
    """
    Summarize the given text using the text-generation pipeline.

    Args:
        text (str): Input content to summarize.

    Returns:
        str: Concise summary or diagnostic message.
    """
    if not text.strip():
        return "⚠️ No content available to summarize."

    if _summarizer_pipeline is None or _tokenizer is None:
        return "🚫 Summarizer pipeline not initialized. Check model and token."

    eos_token_id: Optional[int] = getattr(_tokenizer, "eos_token_id", None)
    if not isinstance(eos_token_id, int):
        return "⚠️ Tokenizer is missing eos_token_id. Cannot enforce stopping criteria."

    prompt = (
        "<|system|>\nYou are a helpful assistant that summarizes text into a few concise sentences."
        "<|user|>\nSummarize the following text:\n\n"
        f"{text}<|assistant|>\n"
    )

    try:
        outputs = _summarizer_pipeline(
            prompt,
            max_new_tokens=150,
            do_sample=False,
            eos_token_id=eos_token_id,
            pad_token_id=eos_token_id,
        )
    except Exception as e:
        return f"🚫 Inference error: {e}"

    generated_text = outputs[0].get("generated_text", "").strip()
    marker = "<|assistant|>\n"
    start = generated_text.rfind(marker)

    summary = (
        generated_text[start + len(marker):].strip()
        if start != -1
        else generated_text.replace(prompt, "").strip()
    )

    return summary or "⚠️ Model returned an empty summary."


# Example usage
if __name__ == "__main__":
    test_input = (
        "Agentic AI refers to artificial intelligence systems that can operate autonomously to achieve goals. "
        "They can plan, remember, and take actions without constant supervision."
    )

    print("--- Original Text ---")
    print(test_input)
    print("\n--- Summary ---")
    print(summarize_text(test_input))
