#!/bin/bash
set -e
#python3 final_extreme_cleaner_data.py
#
#python3 output_tokenizerrrr.py
#python3 output_tokenizerrrr_supplement.py
#python3 output_tokenize.py
python3 input_name_token_all.py
python3 input_code_tokenizerrrr.py
python3 input_code_tokenize.py
python3 congregate_input_data.py
python3 convert_tensor.py
#python3 token_tfidf.py

