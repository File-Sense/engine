#!/bin/bash

# Function to download files into a specified directory
download_files() {
    local base_url=$1
    local -n files=$2
    local dest_dir=$3

    # Ensure the destination directory exists
    mkdir -p "$dest_dir"

    # Loop through the associative array and download each file
    for remote_file in "${!files[@]}"; do
        local_file="${files[$remote_file]}"
        echo "Downloading $remote_file to $dest_dir/$local_file"
        curl -sSL -o "$dest_dir/$local_file" "$base_url/$remote_file"
    done
}

# Base URLs for the files
BASE_URL_CAPTION="https://huggingface.co/Salesforce/blip-image-captioning-base/resolve/main"
BASE_URL_IMAGE="https://huggingface.co/google/vit-base-patch16-224-in21k/resolve/main"
BASE_URL_TEXT="https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1/resolve/main"

# Destination directories
DEST_DIR_CAPTION="./AI/model-caption"
DEST_DIR_IMAGE="./AI/model-image"
DEST_DIR_TEXT="./AI/model-text"

# Declare associative arrays for files to download
declare -A files_caption=(
    ["config.json?download=true"]="config.json"
    ["preprocessor_config.json?download=true"]="preprocessor_config.json"
    ["pytorch_model.bin?download=true"]="pytorch_model.bin"
    ["special_tokens_map.json?download=true"]="special_tokens_map.json"
    ["tokenizer.json?download=true"]="tokenizer.json"
    ["tokenizer_config.json?download=true"]="tokenizer_config.json"
    ["vocab.txt?download=true"]="vocab.txt"
)

declare -A files_image=(
    ["config.json?download=true"]="config.json"
    ["preprocessor_config.json?download=true"]="preprocessor_config.json"
    ["pytorch_model.bin?download=true"]="pytorch_model.bin"
)

declare -A files_text=(
    ["config_sentence_transformers.json?download=true"]="config_sentence_transformers.json"
    ["config.json?download=true"]="config.json"
    ["data_config.json?download=true"]="data_config.json"
    ["modules.json?download=true"]="modules.json"
    ["pytorch_model.bin?download=true"]="pytorch_model.bin"
    ["sentence_bert_config.json?download=true"]="sentence_bert_config.json"
    ["special_tokens_map.json?download=true"]="special_tokens_map.json"
    ["tokenizer_config.json?download=true"]="tokenizer_config.json"
    ["tokenizer.json?download=true"]="tokenizer.json"
    ["vocab.txt?download=true"]="vocab.txt"
)

# Download files for model-caption
echo "Downloading model-caption files..."
download_files "$BASE_URL_CAPTION" files_caption "$DEST_DIR_CAPTION"

# Download files for model-image
echo "Downloading model-image files..."
download_files "$BASE_URL_IMAGE" files_image "$DEST_DIR_IMAGE"

# Download files for model-text
echo "Downloading model-text files..."
download_files "$BASE_URL_TEXT" files_text "$DEST_DIR_TEXT"

echo "Download completed."