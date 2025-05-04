import re
import pandas as pd

# === LLM token count ===
def count_llm_tokens(text, tokenizer):
    tokens = tokenizer.tokenize(text)
    return len(tokens)

# === Semantic Tokenizer (for RDF/OWL terms, NOT LLM tokens) ===
def semantic_tokenize(text):
    tokens = []
    for match in re.findall(r'\b(\w+):(\w+)\b', text):
        tokens.extend(match)
    text_cleaned = re.sub(r'\b\w+:\w+\b', '', text)
    tokens.extend(re.findall(r'\b\w+\b', text_cleaned))
    return tokens

# === Metric: Vocabulary-specific density per line ===
def vocab_specific_density(text, vocab):
    raw_lines = text.splitlines()
    cleaned_lines = [line.strip() for line in raw_lines if line.strip()]
    if not cleaned_lines:
        return 0

    vocab_count = 0

    for line in cleaned_lines:
        literals = {}
        def replacer(m):
            key = f"__LIT{len(literals)}__"
            literals[key] = m.group(0)
            return key

        masked = re.sub(r'"""(.*?)"""', replacer, line, flags=re.DOTALL)
        masked = re.sub(r'"(.*?)"', replacer, masked)
        for key, val in literals.items():
            masked = masked.replace(key, val)

        tokens = re.findall(r'\b\w+:\w+\b', masked) + re.findall(r'\b\w+\b', re.sub(r'\b\w+:\w+\b', '', masked))
        vocab_count += sum(1 for tok in tokens if tok in vocab)

    return vocab_count / len(cleaned_lines)

# === Metric: Vocabulary-specific diversity ===
def vocab_specific_diversity(text, vocab):
    tokens = re.findall(r'\b\w+:\w+\b', text)
    used_vocab_terms = {tok for tok in tokens if tok in vocab}
    return len(used_vocab_terms) / len(vocab) if vocab else 0

# === Metric: Unique Logical Block ratio ===
def logical_block_uniqueness_ratio(text):
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("@")]
    combined_text = " ".join(lines)
    literals = {}
    def replacer(m):
        key = f"__LIT{len(literals)}__"
        literals[key] = m.group(0)
        return key

    masked = re.sub(r'"""(.*?)"""', replacer, combined_text, flags=re.DOTALL)
    masked = re.sub(r'"(.*?)"', replacer, masked)
    phrases = [p.strip() for p in re.split(r'\s*\.\s+', masked) if p.strip()]
    return len(set(phrases)) / len(phrases) if phrases else 0

# === Metric: Unique line ratio ===
def line_uniqueness_ratio(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return len(set(lines)) / len(lines) if lines else 0

# === Metric: Brunet Index (lexical diversity) ===
def brunet_index(text):
    tokens = semantic_tokenize(text)
    N = len(tokens)
    V = len(set(tokens))
    return N ** (V ** -0.165) if V else 0



# Ontology Reference Index (ORI)
def compute_ontology_reference_index(
    df_dataset_path,
    df_llm_path,
    output_path,
    applied_to="dataset"
):
    # Load input datasets
    df_dataset = pd.read_excel(df_dataset_path)
    df_llm = pd.read_excel(df_llm_path)

    # Columns to normalize
    columns_to_normalize = [
        'vocab_specific_density',
        'vocab_specific_diversity',
        'logical_block_uniqueness_ratio',
        'line_uniqueness_ratio',
        'brunet_index'
    ]

    # Normalize dataset columns
    for col in columns_to_normalize:
        min_val = df_dataset[col].min()
        max_val = df_dataset[col].max()
        if max_val != min_val:
            df_dataset[f"norm({col})"] = (df_dataset[col] - min_val) / (max_val - min_val)
        else:
            df_dataset[f"norm({col})"] = 0.0

    # Inverse normalized brunet index
    df_dataset["inv_norm(brunet_index)"] = 1 - df_dataset["norm(brunet_index)"]
    df_dataset.drop(columns=["norm(brunet_index)"], inplace=True)

    # Extract base model metrics
    base_model_vocab_specific_density_per_line = df_llm["vocab_specific_density"].iloc[0]
    base_model_vocab_specific_diversity = df_llm["vocab_specific_diversity"].iloc[0]
    base_model_logical_block_uniqueness_ratio = df_llm["logical_block_uniqueness_ratio"].iloc[0]
    base_model_line_uniqueness_ratio = df_llm["line_uniqueness_ratio"].iloc[0]
    base_model_brunet_index = df_llm["brunet_index"].iloc[0]

    # Best metrics from dataset
    best_onto_vocab_specific_density_per_line = df_dataset["vocab_specific_density"].max()
    best_onto_vocab_specific_diversity = df_dataset["vocab_specific_diversity"].max()
    best_onto_logical_block_uniqueness_ratio = df_dataset["logical_block_uniqueness_ratio"].max()
    best_onto_line_uniqueness_ratio = df_dataset["line_uniqueness_ratio"].max()
    best_onto_brunet_index = df_dataset["brunet_index"].min()

    # Calculate gains
    gain_logical_block_uniqueness_ratio = best_onto_logical_block_uniqueness_ratio / base_model_logical_block_uniqueness_ratio
    gain_line_uniqueness_ratio = best_onto_line_uniqueness_ratio / base_model_line_uniqueness_ratio
    gain_brunet_index = base_model_brunet_index / best_onto_brunet_index
    gain_vocab_specific_density_per_line = best_onto_vocab_specific_density_per_line / base_model_vocab_specific_density_per_line
    gain_vocab_specific_diversity = best_onto_vocab_specific_diversity / base_model_vocab_specific_diversity

    sum_of_gains = (
        gain_logical_block_uniqueness_ratio +
        gain_line_uniqueness_ratio +
        gain_brunet_index +
        gain_vocab_specific_density_per_line +
        gain_vocab_specific_diversity
    )

    # Calculate weights
    weight_logical_block_uniqueness_ratio = gain_logical_block_uniqueness_ratio / sum_of_gains
    weight_line_uniqueness_ratio = gain_line_uniqueness_ratio / sum_of_gains
    weight_brunet_index = gain_brunet_index / sum_of_gains
    weight_vocab_specific_density_per_line = gain_vocab_specific_density_per_line / sum_of_gains
    weight_vocab_specific_diversity = gain_vocab_specific_diversity / sum_of_gains

    # Select working DataFrame
    if applied_to == "dataset":
        final_df = df_dataset.copy()
    elif applied_to == "llm":
        final_df = df_llm.copy()
        for col in columns_to_normalize:
            min_val = df_dataset[col].min() #df_outputs[col].min()
            max_val = df_dataset[col].max() #df_outputs[col].max()
            if max_val != min_val:
                final_df[f"norm({col})"] = (final_df[col] - min_val) / (max_val - min_val)
            else:
                # If constant column, assign 0.0 to all
                final_df[f"norm({col})"] = 0.0

        # Create the inverse normalized column
        final_df["inv_norm(brunet_index)"] = 1 - final_df["norm(brunet_index)"]

        # Drop the original normalized column
        final_df.drop(columns=["norm(brunet_index)"], inplace=True)
    else:
        raise ValueError("Please select 'dataset' or 'llm' for the applied_to argument.")

    # Compute Ontology Reference Index (ORI)
    final_df["ORI"] = 0.0
    for k in range(len(final_df)):
        final_df.at[k, "ORI"] = (
            weight_brunet_index * final_df.at[k, "inv_norm(brunet_index)"] +
            weight_vocab_specific_density_per_line * final_df.at[k, "norm(vocab_specific_density)"] +
            weight_vocab_specific_diversity * final_df.at[k, "norm(vocab_specific_diversity)"] +
            weight_logical_block_uniqueness_ratio * final_df.at[k, "norm(logical_block_uniqueness_ratio)"] +
            weight_line_uniqueness_ratio * final_df.at[k, "norm(line_uniqueness_ratio)"]
        )

    # Save output
    final_df.to_excel(output_path, index=False)
    print(f"Ontology Reference Index saved to {output_path}")