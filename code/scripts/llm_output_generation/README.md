#  README – Ontology Generation with an LLM

This project generates **ontology fragments** using an LLM, **Llama 3.2-1B** by default, based on input prompts. The results are saved in a structured JSON format for further use or evaluation.

---

## How It Works

### Input File: `prompts.json`

The system starts with a JSON file named `prompts.json`. This file contains a list of **ontology fragments**, each paired with its origin. Each item includes:
- A **text snippet** from an ontology.
- The **repository name** (for example, `"edam"` or `"mds-onto"`).

Example:
```json
{
    "citation": {
        "source": "edam",
        "text": "###  http://edamontology.org/citation\n:citation rdf:type owl:AnnotationProperty ..."
    }
}
```

## Step-by-Step Process

**Load input prompts**  
The script reads all entries from `prompts.json` to prepare them for processing.

**Generate multiple outputs per input**  
For every ontology fragment, the model performs six independent generations, ensuring diverse ontology completions.

**Save outputs incrementally**  
As each fragment is processed, the system immediately writes the results to an output file (`generated_ontologies.json`) to avoid losing progress.


## Output File: `generated_ontologies.json`

The final results are written into this JSON file, using keys that combine the input name and a generation index (e.g., `"citation_0"`, `"has_identifier_1"`).

Each entry includes:
- The **original repository source**.
- The **generated ontology text**.

**Example:**
```json
{
    "citation_0": {
        "source": "edam",
        "generated_text": "Generated ontology for citation..."
    },
    "has_identifier_1": {
        "source": "edam",
        "generated_text": "Generated ontology for has_identifier..."
    }
}
```
