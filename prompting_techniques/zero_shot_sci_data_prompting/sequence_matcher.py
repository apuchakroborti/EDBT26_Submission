from difflib import get_close_matches

def traverse_dict(d, path=""):
    """
    A generator function to traverse the dictionary and yield full paths.
    """
    for key, value in d.items():
        current_path = f"{path}/{key}".lstrip("/")
        if isinstance(value, dict):
            # If the value is a nested dictionary, recursively traverse it
            yield from traverse_dict(value, current_path)
        else:
            # If it's not a dictionary, it's a leaf node
            yield current_path

def find_matching_paths(nested_dict, input_text):
    """
    Find matching paths in a nested dictionary based on input text (partial/full/word match).
    """
    # Tokenize input text into words or phrases
    input_tokens = input_text.split()
    
    # Get all possible paths from the dictionary
    all_paths = list(traverse_dict(nested_dict))
    
    matching_paths = set()
    
    # For each token in input text, try to find matching paths
    for token in input_tokens:
        # Get close matches for the token in the list of paths
        matched = get_close_matches(token, all_paths, n=5, cutoff=0.6)
        matching_paths.update(matched)

    return list(matching_paths)

"""# Example usage:
nested_dict = {
    'group1': {
        'subgroup1': {
            'dataset1': {},
            'dataset2': {}
        },
        'subgroup2': {
            'dataset3': {}
        }
    },
    'group2': {
        'dataset4': {}
    }
}

# Input text can be partial paths, full paths, or single words
input_text = "group1 dataset2 group2/dataset4"

# Find matching paths
matches = find_matching_paths(nested_dict, input_text)
print("Matching paths:", matches)
"""