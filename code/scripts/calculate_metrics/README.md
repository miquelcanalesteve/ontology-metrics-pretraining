#  README – Ontology Metrics Toolkit

This repository contains Python scripts to compute various metrics on ontologies (in TTL format) and on LLM-generated texts, and to combine these into a global **Ontology Reference Index (ORI)** score.

---

## 📂 Files Overview

| File                  | Purpose                                                                                                                                       |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `metrics.py`          | Defines core metric functions (e.g., token counts, lexical diversity, uniqueness ratios) and the ORI computation logic.                        |
| `dataset_metrics.py`  | Computes all metrics for a folder of `.ttl` ontology files and outputs the results to an Excel file.                                           |
| `llm_metrics.py`      | Computes the global average metrics over all `generated_text` entries in a JSON file of LLM outputs and saves the result to Excel.         |
| `ori.py`              | Runs the ORI calculation, combining dataset and LLM metrics, and outputs an Excel file with the final ORI scores. **Important:** You must set `applied_to` to `"dataset"` or `"llm"` depending on what you want to score. |

---

## 🔍 Metrics Description

The following metrics are computed in both dataset and LLM evaluations:
- **LLM Token Count**: Number of tokens based on the provided LLM tokenizer.
- **Vocabulary-Specific Density**: Density of occurrences from a predefined vocabulary within the text, measured per line.
- **Vocabulary-Specific Diversity**: Diversity of distinct vocabulary terms used relative to the total vocabulary.
- **Sentence Uniqueness Ratio**: Ratio of unique RDF/OWL triple-like sentences.
- **Line Uniqueness Ratio**: Ratio of unique text lines.
- **Brunet Index**: Lexical diversity score adapted for semantic tokens.
- **Ontology Reference Index**: A combined weighted score that integrates all normalized metrics (density, diversity, uniqueness, and inverse Brunet Index) to provide a single comparative measure of ontology quality relative to the dataset or LLM outputs.

---

## ⚙ How to Use

### 1⃣ Prepare Vocabulary
Make sure you have a `vocab.json` file containing your relevant namespace and terms in the format:
```json
{
    "rdf": ["type", "Property"],
    "rdfs": ["Class", "subClassOf"],
    "owl": ["Thing", "ObjectProperty"],
    "xsd": ["string", "integer"]
}
```

---

### 2⃣ Run Dataset Metrics
Analyze all `.ttl` files in a folder:
```bash
python dataset_metrics.py
```
- Input folder: hardcoded as `/app/data/ttl`
- Output Excel: `/app/outputs/dataset_metrics.xlsx`

---

### 3⃣ Run LLM Metrics
Analyze `generated_text` fields in a JSON:
```bash
python llm_metrics.py
```
- Input JSON: hardcoded as `/app/outputs/generated_ontologies.json`
- Output Excel: `/app/outputs/llm_metrics.xlsx`

---

### 4⃣ Compute Ontology Reference Index (ORI)
Combine the dataset and LLM metrics to get a weighted ORI score:
```bash
python ori.py
```
By default, this runs:
```python
compute_ontology_reference_index(
    df_dataset_path="/app/outputs/dataset_metrics.xlsx",
    df_llm_path="/app/outputs/llm_metrics.xlsx",
    output_path="/app/outputs/dataset_with_ORI.xlsx",
    applied_to="dataset"  # or "llm"
)
```
> **⚠ Important:**  
> You must explicitly set `applied_to` to either:  
> - `"dataset"` → compute ORI for the dataset ontologies  
> - `"llm"` → compute ORI for the LLM-generated results


## 📄 Outputs

| Script                | Output File                                |
|-----------------------|-------------------------------------------|
| `dataset_metrics.py`  | `/app/outputs/dataset_metrics.xlsx`        |
| `llm_metrics.py`      | `/app/outputs/llm_metrics.xlsx`            |
| `ori.py`              | `/app/outputs/dataset_with_ORI.xlsx`       |

---
