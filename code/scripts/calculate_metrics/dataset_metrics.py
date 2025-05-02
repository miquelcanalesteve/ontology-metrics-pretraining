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

# === Process all TTL files in folder ===
def analyze_all_ttl_files(input_folder, output_excel_path, vocab, tokenizer=None):
    new_results = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".ttl"):
            file_path = os.path.join(input_folder, filename)
            print(f"Processing file: {filename}")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                new_results.append({
                    "file": filename,
                    "llm_token_count": count_llm_tokens(text, tokenizer),
                    "vocab_specific_density": vocab_specific_density(text, vocab),
                    "vocab_specific_diversity": vocab_specific_diversity(text, vocab),
                    "sentence_uniqueness_ratio": sentence_uniqueness_ratio(text),
                    "line_uniqueness_ratio": line_uniqueness_ratio(text),
                    "brunet_index": brunet_index(text),
                })
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                new_results.append({"file": filename, **{k: "ERROR" for k in range(10)}})

    if new_results:
        df = pd.DataFrame(new_results)
        df.to_excel(output_excel_path, index=False)
        print(f"All metrics saved to {output_excel_path}")
        return df
    else:
        print("No .ttl files found to process.")
        return None

# === Main Execution ===
if __name__ == "__main__":
    input_folder = "/app/data/ontology_repository"
    output_excel = "/app/outputs/dataset_metrics.xlsx"
    vocab = load_vocab("vocab.json")

    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-3.2-1B",
        use_auth_token="your_token"
    )

    analyze_all_ttl_files(input_folder, output_excel, vocab, tokenizer)
