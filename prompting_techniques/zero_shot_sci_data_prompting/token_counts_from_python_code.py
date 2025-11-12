#!/usr/bin/env python3
"""
pip3 install --upgrade mistral-common

token_counts_from_python_code.py

Counts tokens for files matching a suffix (default "_0.py") in provided directories or via a CSV mapping.
Writes an Excel workbook with a `details` sheet (per-file rows) and a `summary` sheet (per-model max).

Usage examples:
1) List directories:
   python token_counts_from_python_code.py --dirs /data/deepseek-r1:32b /data/llama3:70b --out token_report.xlsx

2) Use CSV mapping (model_name,path):
   python token_counts_from_python_code.py --mapping mapping.csv --out token_report.xlsx

3) Count all .py files:
   python token_counts_from_python_code.py --dirs /data/llama3:70b --file-suffix .py --out llama_tokens.xlsx
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import pandas as pd



def build_tokenizer(model_hint: str = None):
    print(f'build_tokenizer:: model_hint: {model_hint}')

    """
    Returns (tok_count_fn, tokenizer_name). If model_hint contains 'devstral',
    attempt to load Devstral's Tekken tokenizer via transformers / mistral-common.
    """
    # 1) If Devstral, try the model-specific tokenizer
    print(f'build_tokenizer:: model_hint and "devstral" in model_hint.lower() --> {model_hint and "devstral" in model_hint.lower()}')
    
    if model_hint and "devstral" in model_hint.lower():
        print(f'build_tokenizer:: passed model_hint and "devstral" in model_hint.lower()')

        try:
            # Option A: Hugging Face model id (online)
            from transformers import AutoTokenizer
            tok = AutoTokenizer.from_pretrained("mistralai/Devstral-Small-2505", use_fast=True)
            def tok_count(text: str) -> int:
                return len(tok.encode(text))
            
            print(f'build_tokenizer:: huggingface:Devstral-Small-2505')
            return tok_count, "huggingface:Devstral-Small-2505"
        except Exception as e:
            print(f'Exception occured while setting huggingface:Devstral-Small-2505, message: {e} ')
            try:
                # Option B: if the environment needs mistral-common
                # pip install mistral-common
                from mistral_common import TekkenTokenizer
                tek = TekkenTokenizer.from_file("path/to/tekken.json")  # or TekkenTokenizer.from_pretrained(...)
                def tok_count(text: str) -> int:
                    return len(tek.encode(text))
                
                print(f'build_tokenizer:: tekken:devstral-local')
                return tok_count, "tekken:devstral-local"
            except Exception as e:
                print(f'Exception occured while setting tekken:devstral-local, message: {e} ')
                # fall through to general tokenizers below
                pass

    # 2) Existing fallbacks: tiktoken, transformers:gpt2, heuristic...
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        
        print(f'build_tokenizer:: tiktoken:cl100k_base')
       
        return (lambda text: len(enc.encode(text))), "tiktoken:cl100k_base"
    except Exception:
        pass
    try:
        from transformers import GPT2TokenizerFast
        tok = GPT2TokenizerFast.from_pretrained("gpt2")

        print(f'build_tokenizer:: transformers:gpt2')
        return (lambda text: len(tok.encode(text))), "transformers:gpt2"
    except Exception:
        pass
    import re
    
    print(f'build_tokenizer:: heuristic')
    return (lambda text: max(1, len(re.findall(r"\w+|[^\s\w]", text)))), "heuristic"


# def build_tokenizer(model_hint: str = None) -> Tuple[Callable[[str], int], str]:
#     print(f'build_tokenizer:: model_hint: {model_hint}')
#     """
#     Returns (token_count_function, tokenizer_name).
#     Tries tiktoken, then transformers GPT2TokenizerFast, then a simple heuristic.
#     """
#     try:
#         import tiktoken

#         enc_name = "cl100k_base"
#         if model_hint:
#             mn = model_hint.lower()
#             if "gpt2" in mn or "gpt-2" in mn:
#                 enc_name = "gpt2"
#         enc = tiktoken.get_encoding(enc_name)

#         def tok_count(text: str) -> int:
#             return len(enc.encode(text))
        
#         print(f'build_tokenizer:: tiktoken:{enc_name}')
        
#         return tok_count, f"tiktoken:{enc_name}"
#     except Exception:
#         pass

#     try:
#         from transformers import GPT2TokenizerFast

#         tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

#         def tok_count(text: str) -> int:
#             return len(tokenizer.encode(text))

#         print(f'build_tokenizer:: transformers:gpt2')
#         return tok_count, "transformers:gpt2"
#     except Exception:
#         pass

#     def tok_count(text: str) -> int:
#         import re

#         toks = re.findall(r"\w+|[^\s\w]", text, flags=re.UNICODE)
#         return max(1, len(toks))
    
#     print(f'build_tokenizer:: heuristic:whitespace')
#     return tok_count, "heuristic:whitespace"


def load_mapping_csv(path: str) -> List[Tuple[str, str]]:
    """Load CSV mapping with headers model_name,path. Returns list of (model_name, path)."""
    pairs: List[Tuple[str, str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            model = row.get("model_name") or row.get("model") or row.get("name")
            p = row.get("path") or row.get("dir") or row.get("directory")
            if model and p:
                pairs.append((model, p))
    return pairs


def find_files_for_model(directory: str, suffix: str) -> List[Path]:
    """Return list of Path objects for files ending with suffix (recursive)."""
    p = Path(directory)
    if not p.exists():
        return []
    files = [fp for fp in p.rglob(f"*{suffix}") if fp.is_file()]
    return sorted(files)


def compute_tokens_for_directory(
    model_name: str, directory: str, tokenizer_fn: Callable[[str], int], suffix: str
) -> List[Dict]:
    """Compute token counts for all files with the given suffix in directory."""
    rows = []
    files = find_files_for_model(directory, suffix)
    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8")
        except Exception:
            try:
                text = fp.read_text(encoding="latin-1")
            except Exception:
                text = ""
        tokens = tokenizer_fn(text)
        rows.append(
            {
                "model_name": model_name,
                "file_name": str(fp.name),
                "file_path": str(fp),
                "tokens_length": int(tokens),
                "directory_path": str(Path(directory).resolve()),
            }
        )
    return rows


def main():
    parser = argparse.ArgumentParser(description="Count tokens in generated python files.")
    parser.add_argument("--dirs", nargs="*", help="List of directories. Model name inferred from last path segment.")
    parser.add_argument("--mapping", help="CSV file with columns 'model_name,path'")
    parser.add_argument("--out", default="tokens_report.xlsx", help="Output excel filename")
    parser.add_argument("--file-suffix", default="_0.py", help="Suffix to identify files (default _0.py)")
    parser.add_argument("--use-model-hint", action="store_true", help="Pick tokenizer encoding based on model_name (best-effort)")
    args = parser.parse_args()

    file_suffix = args.file_suffix

    mappings: List[Tuple[str, str]] = []

    if args.dirs:
        for d in args.dirs:
            p = Path(d)
            model = p.name
            mappings.append((model, str(p)))

    if args.mapping:
        csv_pairs = load_mapping_csv(args.mapping)
        mappings.extend(csv_pairs)

    if not mappings:
        print("No directories provided. Use --dirs or --mapping.", file=sys.stderr)
        sys.exit(1)

    results = []
    per_model_max: Dict[str, int] = {}

    # When not using model hint, build one generic tokenizer for speed
    # generic_tokenizer_fn, generic_name = build_tokenizer(None)
    generic_tokenizer_fn, generic_name = build_tokenizer('devstral')

    # We want to allow multiple directories mapping to the same model_name.
    # Group directories per model_name
    grouped: Dict[str, List[str]] = {}
    for model_name, directory in mappings:
        grouped.setdefault(model_name, []).append(directory)

    for model_name, dir_list in grouped.items():
        # Choose tokenizer
        if args.use_model_hint:
            tokenizer_fn, tok_name = build_tokenizer(model_name)
        else:
            tokenizer_fn, tok_name = generic_tokenizer_fn, generic_name

        model_rows = []
        for directory in dir_list:
            rows = compute_tokens_for_directory(model_name, directory, tokenizer_fn, file_suffix)
            if not rows:
                print(f"Warning: no files matching '*{file_suffix}' found under {directory} for model {model_name}", file=sys.stderr)
            model_rows.extend(rows)

        max_tokens = max([r["tokens_length"] for r in model_rows], default=0)
        for r in model_rows:
            r["directory_max_tokens"] = int(max_tokens)
            r["tokenizer_used"] = tok_name
        results.extend(model_rows)
        per_model_max[model_name] = int(max_tokens)

    if not results:
        print("No matching files found in any provided directories. Exiting.", file=sys.stderr)
        sys.exit(2)

    df = pd.DataFrame(results)
    cols = ["model_name", "file_name", "file_path", "tokens_length", "directory_max_tokens", "tokenizer_used", "directory_path"]
    existing_cols = [c for c in cols if c in df.columns]
    df = df[existing_cols]

    summary = pd.DataFrame(
        [{"model_name": model, "directory_max_tokens": max_t, "directories": ";".join(grouped[model])} for model, max_t in per_model_max.items()]
    )

    with pd.ExcelWriter(args.out, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="details", index=False)
        summary.to_excel(writer, sheet_name="summary", index=False)

    print(f"Wrote report to {args.out}")
    print(f"Files processed: {len(df)}")
    print("Per-model max tokens:")
    for m, v in per_model_max.items():
        print(f"  {m}: {v}")


if __name__ == "__main__":
    main()



# #!/usr/bin/env python3
# """
# Requirements: pip3 install tiktoken transformers pandas openpyxl

# count_tokens_dir.py

# Usage examples:
# 1) Pass directories directly (model name inferred from directory name):
#    python count_tokens_dir.py --dirs /path/to/deepseek-r1:32b /path/to/devstral:24b --out tokens_report.xlsx

# 2) Provide a CSV mapping (model_name,path) with header:
#    model_name,path
#    deepseek-r1:32b,/path/to/deepseek
#    devstral:24b,/path/to/devstral
#    python count_tokens_dir.py --mapping mapping.csv --out tokens_report.xlsx

# 3) Mix of both:
#    python count_tokens_dir.py --dirs /some/path --mapping mapping.csv --out out.xlsx

# Notes:
# - The script looks for files ending with "_0.py". Change FILE_SUFFIX if you want different.
# - Installs: pip install tiktoken transformers pandas openpyxl
# """

# import argparse
# import csv
# import os
# import sys
# from pathlib import Path
# from typing import Callable, Dict, List, Tuple

# import pandas as pd

# FILE_SUFFIX = "_0.py"


# def build_tokenizer(model_hint: str = None) -> Tuple[Callable[[str], int], str]:
#     """
#     Try to create a tokenizer function that returns the number of tokens for a text.
#     Returns (token_count_function, tokenizer_name)
#     Fallback order:
#       1. tiktoken (best accuracy for many modern models)
#       2. transformers GPT2TokenizerFast
#       3. whitespace heuristic
#     model_hint may be used to choose encoding (best-effort).
#     """
#     # Attempt tiktoken
#     try:
#         import tiktoken

#         # heuristic mapping: for many modern models use cl100k_base; for older/gpt2 use gpt2
#         enc_name = "cl100k_base"
#         if model_hint:
#             mn = model_hint.lower()
#             if "gpt2" in mn or "gpt-2" in mn or "gpt2" in mn:
#                 enc_name = "gpt2"
#             # Llama / other tokenizers unknown -- cl100k_base is a reasonable default for many.
#         enc = tiktoken.get_encoding(enc_name)

#         def tok_count(text: str) -> int:
#             return len(enc.encode(text))

#         return tok_count, f"tiktoken:{enc_name}"
#     except Exception:
#         pass

#     # Attempt transformers' GPT2TokenizerFast
#     try:
#         from transformers import GPT2TokenizerFast

#         tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

#         def tok_count(text: str) -> int:
#             return len(tokenizer.encode(text))

#         return tok_count, "transformers:gpt2"
#     except Exception:
#         pass

#     # Final fallback: simple whitespace/punctuation heuristic (low-accuracy)
#     def tok_count(text: str) -> int:
#         # split on whitespace and punctuation - simple heuristic
#         import re

#         toks = re.findall(r"\w+|[^\s\w]", text, flags=re.UNICODE)
#         return max(1, len(toks))

#     return tok_count, "heuristic:whitespace"


# def load_mapping_csv(path: str) -> Dict[str, str]:
#     """Load CSV mapping with headers model_name,path"""
#     mapping = {}
#     with open(path, newline="", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             model = row.get("model_name") or row.get("model") or row.get("name") or row.get("modelName")
#             p = row.get("path") or row.get("dir") or row.get("directory")
#             if model and p:
#                 mapping[model] = p
#     return mapping


# # def find_files_for_model(directory: str, suffix: str = FILE_SUFFIX) -> List[Path]:
# #     """Return list of Path objects for files ending with suffix (non-recursive)."""
# #     p = Path(directory)
# #     if not p.exists():
# #         return []
# #     files = []
# #     # We'll do a recursive search (descend into subdirectories) because files can be nested.
# #     for fp in p.rglob(f"*{suffix}"):
# #         if fp.is_file():
# #             files.append(fp)
# #     return sorted(files)


# # def compute_tokens_for_directory(model_name: str, directory: str, tokenizer_fn: Callable[[str], int]) -> List[Dict]:
# #     rows = []
# #     files = find_files_for_model(directory)
# #     for fp in files:
# #         try:
# #             text = fp.read_text(encoding="utf-8")
# #         except Exception:
# #             try:
# #                 text = fp.read_text(encoding="latin-1")
# #             except Exception:
# #                 text = ""
# #         tokens = tokenizer_fn(text)
# #         rows.append(
# #             {
# #                 "model_name": model_name,
# #                 "file_name": str(fp.name),
# #                 "file_path": str(fp),
# #                 "tokens_length": int(tokens),
# #                 "directory_path": str(Path(directory).resolve()),
# #             }
# #         )
# #     return rows

# def find_files_for_model(directory: str, suffix: str = "_0.py") -> List[Path]:
#     """Return list of Path objects for files ending with suffix (recursive)."""
#     p = Path(directory)
#     if not p.exists():
#         return []
#     files = [fp for fp in p.rglob(f"*{suffix}") if fp.is_file()]
#     return sorted(files)


# def compute_tokens_for_directory(model_name: str, directory: str, tokenizer_fn: Callable[[str], int], suffix: str) -> List[Dict]:
#     """Compute token counts for all files with the given suffix in directory."""
#     rows = []
#     files = find_files_for_model(directory, suffix)
#     for fp in files:
#         try:
#             text = fp.read_text(encoding="utf-8")
#         except Exception:
#             try:
#                 text = fp.read_text(encoding="latin-1")
#             except Exception:
#                 text = ""
#         tokens = tokenizer_fn(text)
#         rows.append(
#             {
#                 "model_name": model_name,
#                 "file_name": str(fp.name),
#                 "file_path": str(fp),
#                 "tokens_length": int(tokens),
#                 "directory_path": str(Path(directory).resolve()),
#             }
#         )
#     return rows


# def main():
#     parser = argparse.ArgumentParser(description="Count tokens in generated python files ending with _0.py")
#     parser.add_argument(
#         "--dirs",
#         nargs="*",
#         help="List of directories. If you pass paths that include model names (like '.../deepseek-r1:32b'), the last path segment will be used as model_name.",
#     )
#     parser.add_argument(
#         "--mapping",
#         help="CSV file with columns 'model_name,path' mapping each model to a directory.",
#     )
#     parser.add_argument("--out", default="tokens_report.xlsx", help="Output excel filename")
#     parser.add_argument("--file-suffix", default=FILE_SUFFIX, help="Suffix to identify files (default _0.py)")
#     parser.add_argument("--use-model-hint", action="store_true", help="Try to pick tokenizer encoding based on model_name (best-effort)")
#     args = parser.parse_args()

#     global FILE_SUFFIX
#     FILE_SUFFIX = args.file_suffix

#     mappings: Dict[str, str] = {}

#     if args.dirs:
#         for d in args.dirs:
#             # If dir string contains a model_name:path format (user example used colon in model names),
#             # attempt to separate "model_name:..."? We'll be conservative: treat the last path segment as model name.
#             p = Path(d)
#             model = p.name
#             # if the path contains an explicit model label like "modelname=/some/path" we won't parse that,
#             # user should use mapping csv in that case.
#             mappings[model] = str(p)

#     if args.mapping:
#         csv_map = load_mapping_csv(args.mapping)
#         # CSV entries override any duplicate keys from --dirs
#         mappings.update(csv_map)

#     if not mappings:
#         print("No directories provided. Use --dirs or --mapping.", file=sys.stderr)
#         sys.exit(1)

#     # Prepare global tokenizer (we will create per-model tokenizer if use_model_hint requested)
#     # If use_model_hint: create per model tokenizer; else create one generic tokenizer.
#     results = []
#     per_model_max = {}

#     # Create a generic tokenizer once (no hint)
#     generic_tokenizer_fn, generic_name = build_tokenizer(None)

#     for model_name, directory in mappings.items():
#         if args.use_model_hint:
#             tokenizer_fn, tok_name = build_tokenizer(model_name)
#         else:
#             tokenizer_fn, tok_name = generic_tokenizer_fn, generic_name

#         rows = compute_tokens_for_directory(model_name, directory, tokenizer_fn)
#         if not rows:
#             print(f"Warning: no files matching '*{FILE_SUFFIX}' found under {directory} for model {model_name}", file=sys.stderr)
#         # compute max tokens
#         max_tokens = max([r["tokens_length"] for r in rows], default=0)
#         for r in rows:
#             r["directory_max_tokens"] = int(max_tokens)
#             r["tokenizer_used"] = tok_name
#         results.extend(rows)
#         per_model_max[model_name] = int(max_tokens)

#     if not results:
#         print("No matching files found in any provided directories. Exiting.", file=sys.stderr)
#         sys.exit(2)

#     df = pd.DataFrame(results)
#     # Reorder columns
#     cols = ["model_name", "file_name", "file_path", "tokens_length", "directory_max_tokens", "tokenizer_used", "directory_path"]
#     existing_cols = [c for c in cols if c in df.columns]
#     df = df[existing_cols]

#     # Write to Excel with two sheets: details and summary
#     summary = pd.DataFrame(
#         [
#             {"model_name": model, "directory_max_tokens": max_t, "directory_path": str(mappings[model])}
#             for model, max_t in per_model_max.items()
#         ]
#     )
#     with pd.ExcelWriter(args.out, engine="openpyxl") as writer:
#         df.to_excel(writer, sheet_name="details", index=False)
#         summary.to_excel(writer, sheet_name="summary", index=False)

#     print(f"Wrote report to {args.out}")
#     print(f"Files processed: {len(df)}")
#     print("Per-model max tokens:")
#     for m, v in per_model_max.items():
#         print(f"  {m}: {v}")


# if __name__ == "__main__":
#     main()
