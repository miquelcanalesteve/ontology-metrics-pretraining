from metrics import compute_ontology_reference_index

compute_ontology_reference_index(
    df_dataset_path="/app/outputs/dataset_metrics.xlsx",
    df_llm_path="/app/outputs/llm_metrics.xlsx",
    output_path="/app/outputs/dataset_with_ORI.xlsx",
    applied_to="dataset" #or "dataset"
)
