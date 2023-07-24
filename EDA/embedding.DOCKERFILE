FROM semitechnologies/transformers-inferece:custom
RUN MODEL_NAME=all_datasets_v4_MiniLM-L6 ./download.py