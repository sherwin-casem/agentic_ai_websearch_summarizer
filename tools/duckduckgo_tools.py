from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model(model_name="cognitivecomputations/TinyLlama-1.1B-Chat-v1.0"):
    """
    Load the instruct-tuned LLM model and tokenizer from Hugging Face.

    Args:
        model_name (str): The name of the model to load from Hugging Face.

    Returns:
        model: The loaded model.
        tokenizer: The loaded tokenizer.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

# Example usage
if __name__ == "__main__":
    model, tokenizer = load_model()
    print("✅ Model and tokenizer loaded successfully.")
