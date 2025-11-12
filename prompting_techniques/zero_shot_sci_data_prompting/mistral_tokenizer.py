def build_tokenizer(model_hint: str = None):
    print(f'build_tokenizer:: model_hint: {model_hint}')
    """
    Robust tokenizer builder:
      1. If model_hint contains 'devstral', try HF AutoTokenizer with trust_remote_code.
      2. If that fails, try to locate local tokenizer files (tokenizer.json or tekken.json)
         and load them with the `tokenizers` library.
      3. Fallbacks: tiktoken, transformers GPT2TokenizerFast, heuristic.
    Returns: (token_count_fn, tokenizer_name)
    """
    import os
    import sys
    import traceback

    def debug(msg):
        # change to print -> ensures visible in console
        print(f"[build_tokenizer] {msg}", file=sys.stderr)

    # Helper: wrap a tokenizer object's encode call into a counting function
    def wrap_tokenizer_obj(obj, encode_fn_name="encode"):
        def tok_count(text: str) -> int:
            if not text:
                return 0
            fn = getattr(obj, encode_fn_name)
            # Some tokenizers return list of ids, some return dicts; handle common cases:
            try:
                out = fn(text)
            except TypeError:
                # some tokenizers require add_special_tokens arg
                out = fn(text, add_special_tokens=False)
            # if HF tokenizer returns BatchEncoding, call .input_ids or len()
            if hasattr(out, "__len__") and not isinstance(out, dict):
                return len(out)
            if isinstance(out, dict) and "input_ids" in out:
                return len(out["input_ids"])
            # fallback
            return int(out) if isinstance(out, int) else 0

        return tok_count

    # 1) If model looks like devstral, try HF AutoTokenizer with trust_remote_code
    if model_hint and "devstral" in model_hint.lower():
        model_id = None
        # common HF ids to try — change/extend if you know a specific id
        candidates = ["mistralai/Devstral-Small-2505", "mistralai/Devstral-Small"]
        for cand in candidates:
            try:
                debug(f"Trying AutoTokenizer.from_pretrained('{cand}', use_fast=True, trust_remote_code=True)")
                from transformers import AutoTokenizer

                tok = AutoTokenizer.from_pretrained(cand, use_fast=True, trust_remote_code=True)
                debug(f"Loaded tokenizer from HF id '{cand}' (class {tok.__class__.__name__})")
                return wrap_tokenizer_obj(tok, "encode"), f"huggingface:{cand}"
            except Exception as e:
                debug(f"Exception occured while setting huggingface:{cand}, message: {e}")
                debug(traceback.format_exc())

        # Also check if a local directory exists with a tekken.json or tokenizer.json close to cwd or model_hint path
        # Common local places to check: current dir, './models/<model_hint>', './<model_hint>'
        potential_paths = [
            model_hint,
            os.path.join(".", model_hint),
            os.path.join("models", model_hint),
            os.path.join("models", model_hint.replace("/", "_")),
        ]
        # Also check environment variable or typical model folder names
        for p in potential_paths:
            if p and os.path.isdir(p):
                debug(f"Found local directory candidate: {p} - listing files:")
                try:
                    for fn in os.listdir(p):
                        debug(f"  - {fn}")
                except Exception:
                    pass

    # 2) Try to find local tokenizer files (tokenizer.json or tekken.json) and use tokenizers library
    try:
        from tokenizers import Tokenizer as HFTokenizer
        import glob

        # search common local tokenizer filenames in cwd and ./models
        search_dirs = [".", "./models"]
        found_file = None
        for d in search_dirs:
            for name in ("tokenizer.json", "tekken.json", "vocab.json", "tokenizer.model"):
                candidate = os.path.join(d, name)
                if os.path.isfile(candidate):
                    found_file = candidate
                    break
            if found_file:
                break

        if not found_file:
            # try any tokenizer file deeper in ./models
            for root, dirs, files in os.walk("./models"):
                for f in files:
                    if f.lower() in ("tokenizer.json", "tekken.json", "vocab.json", "tokenizer.model"):
                        found_file = os.path.join(root, f)
                        break
                if found_file:
                    break

        if found_file:
            debug(f"Trying to load local tokenizer file: {found_file} using tokenizers.Tokenizer.from_file")
            tk = HFTokenizer.from_file(found_file)
            # tokenizers.Tokenizer.encode returns an Encoding object which has .ids or .tokens
            def tok_count_from_tokenizers(text: str) -> int:
                if not text:
                    return 0
                enc = tk.encode(text)
                return len(enc.ids) if hasattr(enc, "ids") else len(enc.tokens)
            return tok_count_from_tokenizers, f"tokenizers_file:{os.path.basename(found_file)}"
    except Exception as e:
        debug(f"Local tokenizers loader failed: {e}")
        # don't raise — continue to fallbacks
        debug(traceback.format_exc())

    # 3) Try tiktoken (good general fallback)
    try:
        import tiktoken

        enc_name = "cl100k_base"
        try:
            enc = tiktoken.get_encoding(enc_name)
            debug(f"Using tiktoken encoding '{enc_name}'")
            return (lambda text: len(enc.encode(text))), f"tiktoken:{enc_name}"
        except Exception as e:
            debug(f"tiktoken.get_encoding failed for {enc_name}: {e}")
    except Exception as e:
        debug(f"tiktoken import failed: {e}")

    # 4) Try transformers GPT-2 tokenizer
    try:
        from transformers import GPT2TokenizerFast

        tok = GPT2TokenizerFast.from_pretrained("gpt2")
        debug("Using transformers GPT2TokenizerFast as fallback")
        return wrap_tokenizer_obj(tok, "encode"), "transformers:gpt2"
    except Exception as e:
        debug(f"transformers GPT2 tokenizer failed: {e}")

    # 5) Final fallback: heuristic
    import re

    debug("Falling back to heuristic token count")
    def heuristic_count(text: str) -> int:
        toks = re.findall(r"\w+|[^\s\w]", text, flags=re.UNICODE)
        return max(1, len(toks))

    return heuristic_count, "heuristic:whitespace"



import argparse
import csv
import sys
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import pandas as pd



# def build_tokenizer(model_hint: str = None):
#     print(f'build_tokenizer:: model_hint: {model_hint}')

#     """
#     Returns (tok_count_fn, tokenizer_name). If model_hint contains 'devstral',
#     attempt to load Devstral's Tekken tokenizer via transformers / mistral-common.
#     """
#     # 1) If Devstral, try the model-specific tokenizer
#     print(f'build_tokenizer:: model_hint and "devstral" in model_hint.lower() --> {model_hint and "devstral" in model_hint.lower()}')
    
#     if model_hint and "devstral" in model_hint.lower():
#         print(f'build_tokenizer:: passed model_hint and "devstral" in model_hint.lower()')

#         try:
#             # Option A: Hugging Face model id (online)
#             from transformers import AutoTokenizer
#             tok = AutoTokenizer.from_pretrained("mistralai/Devstral-Small-2505", use_fast=True)
#             def tok_count(text: str) -> int:
#                 return len(tok.encode(text))
            
#             print(f'build_tokenizer:: huggingface:Devstral-Small-2505')
#             return tok_count, "huggingface:Devstral-Small-2505"
#         except Exception as e:
#             print(f'Exception occured while setting huggingface:Devstral-Small-2505, message: {e} ')
#             try:
#                 # Option B: if the environment needs mistral-common
#                 # pip install mistral-common
#                 from mistral_common import TekkenTokenizer
#                 tek = TekkenTokenizer.from_file("path/to/tekken.json")  # or TekkenTokenizer.from_pretrained(...)
#                 def tok_count(text: str) -> int:
#                     return len(tek.encode(text))
                
#                 print(f'build_tokenizer:: tekken:devstral-local')
#                 return tok_count, "tekken:devstral-local"
#             except Exception as e:
#                 print(f'Exception occured while setting tekken:devstral-local, message: {e} ')
#                 # fall through to general tokenizers below
#                 pass

#     # 2) Existing fallbacks: tiktoken, transformers:gpt2, heuristic...
#     try:
#         import tiktoken
#         enc = tiktoken.get_encoding("cl100k_base")
        
#         print(f'build_tokenizer:: tiktoken:cl100k_base')
       
#         return (lambda text: len(enc.encode(text))), "tiktoken:cl100k_base"
#     except Exception:
#         pass
#     try:
#         from transformers import GPT2TokenizerFast
#         tok = GPT2TokenizerFast.from_pretrained("gpt2")

#         print(f'build_tokenizer:: transformers:gpt2')
#         return (lambda text: len(tok.encode(text))), "transformers:gpt2"
#     except Exception:
#         pass
#     import re
    
#     print(f'build_tokenizer:: heuristic')
#     return (lambda text: max(1, len(re.findall(r"\w+|[^\s\w]", text)))), "heuristic"


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

