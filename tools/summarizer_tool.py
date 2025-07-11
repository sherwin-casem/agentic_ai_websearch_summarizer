# tools/summarizer_tool.py

from typing import Optional
from transformers import pipeline, PreTrainedModel, PreTrainedTokenizerBase
from models.load_model import load_model

# --- Global Setup ---
# Update the model name to the new lightweight model
_model: Optional[PreTrainedModel]
_tokenizer: Optional[PreTrainedTokenizerBase]
_model, _tokenizer = load_model(
    model_name="HuggingFaceTB/SmolLM2-135M-Instruct",
    model_type="causal"
)

_summarizer_pipeline = None
if _model and _tokenizer:
    _summarizer_pipeline = pipeline(
        "text-generation",
        model=_model,
        tokenizer=_tokenizer,
    )
# --- End Global Setup ---


def summarize_text(text: str) -> str:
    """
    Summarize the given text using the text-generation pipeline.
    """
    if not text.strip():
        return "⚠️ No content available to summarize."

    if not _summarizer_pipeline or not _tokenizer:
        return "🚫 Summarizer pipeline not initialized. Check model and token."

    # Use the specific chat template required by SmolLM2 for best results
    prompt = (
        f"<|im_start|>system\n"
        f"You are a helpful assistant that summarizes text into a few concise sentences.<|im_end|>\n"
        f"<|im_start|>user\n"
        f"Summarize the following text:\n\n{text}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )
    
    # Ensure the pipeline knows when to stop generating
    eos_token_id = _tokenizer.eos_token_id

    try:
        outputs = _summarizer_pipeline(
            prompt,
            max_new_tokens=150,  # Max length of the summary
            do_sample=False,     # Use greedy decoding for deterministic output
            eos_token_id=eos_token_id,
            pad_token_id=eos_token_id,
        )
        generated_text = outputs[0].get("generated_text", "").strip()
        
        # Extract only the assistant's response, which comes after the final marker
        marker = "<|im_start|>assistant\n"
        summary = generated_text.split(marker)[-1].strip()
        
        return summary or "⚠️ Model returned an empty summary."

    except Exception as e:
        return f"🚫 Inference error: {e}"

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
