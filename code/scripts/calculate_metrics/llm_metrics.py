import os
import json
import pandas as pd
from transformers import AutoTokenizer
from metrics import (
    count_llm_tokens,
    vocab_specific_density,
    vocab_specific_diversity,
    sentence_uniqueness_ratio,
    line_uniqueness_ratio,
    brunet_index
)

# === Load vocabulary from JSON ===
def load_vocab(json_path="vocab.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        vocab_data = json.load(f)
    vocab = {f"{ns}:{term}" for ns, terms in vocab_data.items() for term in terms}
    return vocab

# === Analyze generated_text values and compute global average ===
def analyze_generated_texts_global_average(input_json_path, output_excel_path, vocab, tokenizer=None):
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for key, entry in data.items():
        text = entry.get("generated_text", "")
        try:
            result = {
                "vocab_specific_density": vocab_specific_density(text, vocab),
                "vocab_specific_diversity": vocab_specific_diversity(text, vocab),
                "sentence_uniqueness_ratio": sentence_uniqueness_ratio(text),
                "line_uniqueness_ratio": line_uniqueness_ratio(text),
                "brunet_index": brunet_index(text),
            }
        except Exception as e:
            print(f"Error processing {key}: {e}")
            result = {metric: None for metric in [
                "llm_token_count", "vocab_specific_density", "vocab_specific_diversity",
                "sentence_uniqueness_ratio", "line_uniqueness_ratio", "brunet_index"
            ]}

        results.append(result)

    df = pd.DataFrame(results)

    # Compute global average (excluding NaNs)
    global_avg = df.mean(numeric_only=True)

    # Convert to single-row DataFrame for saving
    avg_df = pd.DataFrame([global_avg])
    avg_df.to_excel(output_excel_path, index=False)

    print(f"Global average metrics saved to {output_excel_path}")
    return avg_df

# === Main Execution ===
if __name__ == "__main__":
    input_json = "/app/outputs/generated_ontologies.json"
    output_excel = "/app/outputs/llm_metrics.xlsx"
    vocab = load_vocab("vocab.json")

    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-3.2-1B",
        use_auth_token="your_token"
    )

    analyze_generated_texts_global_average(input_json, output_excel, vocab, tokenizer)
