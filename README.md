# Improving Ontology Generation in LLMs through Continual Pretraining and Fast Quality Evaluation

## Overview

This repository provides a complete pipeline to:
- **Generate ontology fragments using an LLM** (default: Llama 3.2-1B)
- **Calculate detailed metrics** over both real ontology datasets and LLM-generated outputs
- **Compute the Ontology Reference Index (ORI)**, which combines multiple normalized metrics to rank and compare ontologies

---

## 📦 Repository Structure

- **`code/` folder** → Main working folder, containing:
    - **`data/`** → Three sample ontologies for testing
    - **`outputs/`** → Results generated from the example ontologies and LLM outputs
    - **`scripts/`** → Core scripts:
        - `calculate_metrics` → Includes `metrics.py`, `dataset_metrics.py`, `llm_metrics.py`, `ori.py` for metric calculations and ORI computation
        - `llm_output_generation` → Runs the LLM to generate ontology fragments from prompts

- **`/results` folder** → Contains main outputs obtained over the full dataset (1766 ontologies from DBpedia Archivo):
    - `full_dataset_with_ORI.xlsx` → Complete dataset with all metrics and ORI
    - `llm_with_ORI.xlsx` → Base and trained LLM results with ORI
    - `manual_evaluation.xlsx` → Annotated manual evaluation of triple-level errors

---

## 🔍 Workflow: Metrics & ORI Calculation

1️⃣ **Run Ontology Generation**  
Input file: `prompts.json` → Output file: `generated_ontologies.json`  
- For each ontology fragment in `prompts.json`, the LLM generates **six** independent completions.
- Example input:
    ```json
    {
        "citation": {
            "source": "edam",
            "text": ":citation rdf:type owl:AnnotationProperty ..."
        }
    }
    ```
- Example output:
    ```json
    {
        "citation_0": {
            "source": "edam",
            "generated_text": "Generated ontology for citation..."
        }
    }
    ```

2️⃣ **Compute Dataset Metrics**  
Run `dataset_metrics.py` to process `.ttl` files and calculate metrics.

3️⃣ **Compute LLM Metrics**  
Run `llm_metrics.py` on the generated outputs to calculate average metrics.

4️⃣ **Calculate ORI**  
Run `ori.py` to combine dataset and LLM metrics into the **Ontology Reference Index (ORI)**, providing a comparative weighted score.

---

## 🐳 Docker Setup

- Includes a **Docker Compose** (`docker-compose.yml`) with GPU support
- Uses `docker/Dockerfile` + `requirements.txt` (Python 3.10, pandas, rdflib, transformers, torch, etc.)
- Mounts scripts, data, and outputs for easy manual runs

---

## ⚠ Disclaimer

The three sample ontologies included in the `code/data` folder are **for demonstration only**. While you can run the full pipeline on these examples, the ORI values will **not match** the main results because the normalization step depends on the full dataset (1766 ontologies from DBpedia Archivo). The `outputs` folder inside `code/` contains example results computed only on these samples and the generated LLM outputs. These are intended for testing and illustration, not for full-scale evaluation.

---
