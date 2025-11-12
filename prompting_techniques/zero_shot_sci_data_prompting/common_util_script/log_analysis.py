import os
import re
import csv

def analyze_log_and_save_to_csv(log_file_path, output_csv_path):
    with open(log_file_path, 'r') as f:
        log_lines = f.readlines()

    results = {}
    current_script = None

    for idx, line in enumerate(log_lines):
        line = line.strip()

        # Match running script line
        if line.startswith("Running Script base name:"):
            current_script = line.split(":")[-1].strip()
            if current_script not in results:
                results[current_script] = {
                    'status': 'Fail',  # default unless we find a pass
                    'png_files': [],
                    'half_name': '',
                    'stderr': '',
                }

        # Look for list of PNG files
        if current_script and "All PNG files with only file names:" in line:
            match = re.findall(r"\[([^\]]+)\]", line)
            if match:
                files = [f.strip().strip("'") for f in match[0].split(',')]
                results[current_script]['png_files'] = files

        # Half file name
        if current_script and "Half file name:" in line:
            results[current_script]['half_name'] = line.split("Half file name:")[-1].strip()

        # Image Found for
        if current_script and "Image Found for:" in line:
            # Not strictly needed since it repeats `half_name`, but could verify match
            pass

        # Execution result
        if current_script and "Execution result:" in line:
            # Next lines include status and stderr
            if idx + 1 < len(log_lines) and "status: Pass" in log_lines[idx + 1]:
                results[current_script]['status'] = 'Pass'
            if idx + 2 < len(log_lines) and "stderr:" in log_lines[idx + 2]:
                stderr = log_lines[idx + 2].split("stderr:")[-1].strip()
                results[current_script]['stderr'] = stderr

    # Identify _0 files that failed and were not retried
    zero_files = [k for k in results if k.endswith('_0')]
    retried_files = set(k.rsplit('_', 1)[0] for k in results if not k.endswith('_0'))

    for base in zero_files:
        root_name = base.rsplit('_', 1)[0]
        if results[base]['status'] == 'Fail' and root_name not in retried_files:
            results[base]['note'] = 'Failed and not retried'
        else:
            results[base]['note'] = ''

    # Write to CSV
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['script_name', 'status', 'stderr', 'png_files', 'half_name', 'note']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for script_name, info in sorted(results.items()):
            writer.writerow({
                'script_name': script_name,
                'status': info['status'],
                'stderr': info['stderr'],
                'png_files': '; '.join(info['png_files']),
                'half_name': info['half_name'],
                'note': info.get('note', '')
            })

    print(f"✅ Analysis complete. CSV saved to: {output_csv_path}")

log_file_path = '/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/iteration_python_code_evaluation_logs/devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector.log'
output_csv_path = f'/home/achakroborti1/llam_test/code-generation-by-llm-for-scientific-data/prompting_techniques/zero_shot_sci_data_prompting/log_analysis_results/{os.path.basename(log_file_path)}.csv'
analyze_log_and_save_to_csv(log_file_path, output_csv_path)