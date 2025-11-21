import subprocess
import csv
import glob
import torch
import torchvision.transforms as transforms
from scipy.spatial.distance import cosine
import os
from pathlib import Path
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from torchvision import models, transforms


# 
def run_python_script_for_evaluation_for_matplot_agent_fastmri_brain(script_path):
    """
    Runs a Python script with the specified HDF5 file as an argument.
    
    Args:
        script_path (str): Path to the Python script.
        data_file (str): Path to the HDF5 file.
    
    Returns:
        tuple: (status, error_message) where status is 'Pass' or 'Fail', and error_message is the error string or None.
    """
    try:
        # Run the Python script with the HDF5 file as an argument
        result = subprocess.run(['python3', script_path], check=True, capture_output=True, text=True)
        return 'Pass', None
    except PermissionError:
        print('Permission error is overlooked')
        return 'Pass', None
    except subprocess.CalledProcessError as e:
        print(f'Fail from subprocess.CalledProcessError, error: {e.stderr}')
        return 'Fail', e.stderr  # If an error occurs, return 'Fail' and the error message
    except Exception as e:
        print(f'Fail from Exception, error: {e}')
        return 'Fail', e
# 
def get_python_files_dict(directory):
    print(f'Script directory for evaluation:\n{directory}')
    directory = os.path.abspath(directory)  # Ensure absolute path
    pattern = os.path.join(directory, "*.py")
    py_scripts = {}  # Dictionary to store results
    for file in glob.glob(pattern):  # Iterate over matching files
        base_name = os.path.splitext(os.path.basename(file))[0]  # Get base filename
        py_scripts[base_name] = file  # Store full path

    return py_scripts

# 
def execute_python_scripts(python_scripts_directory):
    try:
        python_files_dict = get_python_files_dict(python_scripts_directory)
        py_scripts = python_files_dict
        
        for py_script in py_scripts:
                script_path = py_scripts[py_script]
                print(f'Script path: {script_path}')
             
                python_script_file_base_name = os.path.basename(py_script)
                print(f'Script base name: {os.path.basename(py_script)} ')
                status, stderr = run_python_script_for_evaluation_for_matplot_agent_fastmri_brain(script_path)
                print(f'Status: {status}, stderr: {stderr}')

    except Exception as e:
        print(f'Exception occurred while running python scripts, error message: {e}')


import shutil
from pathlib import Path

def collect_and_store_png(source_dirs, target_dir):
    print(f'target dir: {target_dir}')

    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Saving PNG files to: {target_dir}")

    # Collect and copy PNG files
    for directory in source_dirs:
        directory = Path(directory).resolve()
        print("Directory: ", directory)
        if directory.exists():
            for png_file in directory.glob("*.png"):  # Search for PNG files
                print(f'Moving file {png_file} to {target_dir / png_file.name}')
                shutil.move(png_file, target_dir / png_file.name)  # Copy to target

    print("PNG collection and transfer complete!")
# 
def image_to_embedding(image_path, model, preprocess):
    """Convert an image to a feature embedding"""
    image = Image.open(image_path).convert('RGB')
    input_tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        embedding = model(input_tensor).squeeze().numpy()
    return embedding
# 
def calculate_cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    similarity = cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]
    return similarity

# 
def get_name_similarity(name1, name2):
    name1 = name1.lower()
    name2 = name2.lower()
    """Calculate sequential name similarity from the beginning of the string"""
    min_len = min(len(name1), len(name2))
    match_count = 0
    for i in range(min_len):
        if name1[i] == name2[i]:
            match_count += 1
        else:
            break
    return match_count / max(len(name1), len(name2))

def get_id_similarity(name1, name2):
    """Calculate ID name similarity from the beginning of the string"""
    name1_list = name1.split('_')
    name2_list = name2.split('_')
    if len(name1_list)>0 and len(name2_list)>0:
        if name1_list[0] == name2_list[0]:
            return True
    return False
    

def generate_and_save_similarity_scores(input_dir1, input_dir2, target_dir):
    input_dir1 = Path(input_dir1)
    input_dir2 = Path(input_dir2)
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Find all PNG images
    images1 = list(input_dir1.glob('*.png'))
    images2 = list(input_dir2.glob('*.png'))

    # Load a pretrained model for feature extraction
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Identity()  # Remove final classification layer
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    output_csv = target_dir / 'similarity_results.csv'
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Base Image', 'Generated Image', 'Similarity Raw', 'Similarity (%)'])

        for img1 in images1:
            name1 = img1.stem.lower()

            for img2 in images2:
                name2 = img2.stem.lower()
                name_match = get_name_similarity(name1, name2)

                if name_match >= 0.5:
                    # Compute embeddings
                    embedding1 = image_to_embedding(img1, model, preprocess)
                    embedding2 = image_to_embedding(img2, model, preprocess)

                    # Calculate similarity
                    similarity_raw = calculate_cosine_similarity(embedding1, embedding2)
                    similarity_percent = similarity_raw * 100

                    # Write to CSV
                    writer.writerow([img1.name, img2.name, round(similarity_raw, 4), round(similarity_percent, 2)])

    print(f"Similarity results saved to: {output_csv}")


def generate_and_save_iterative_matplotagent_fastmribrain_similarity_scores(input_dir1, input_dir2, target_dir):
    input_dir1 = Path(input_dir1)
    # input_dir2 = Path(input_dir2)
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Find all PNG images
    images1 = list(input_dir1.glob('*.png'))
    # images2 = list(input_dir2.glob('*.png'))

    # Load a pretrained model for feature extraction
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Identity()  # Remove final classification layer
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    for iteration in range(0, 7):
        output_csv = target_dir / f'similarity_results_{iteration}.csv'
        input_dir2_iteration = input_dir2+'_'+str(iteration)
        input_dir2_iteration = Path(input_dir2_iteration)
        images2 = list(input_dir2_iteration.glob('*.png'))

        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Base Image', 'Generated Image', 'Similarity Raw', 'Similarity (%)'])

            for img1 in images1:
                name1 = img1.stem.lower()

                matched = False
                for img2 in images2:
                    name2 = img2.stem.lower()
                    name_match = get_id_similarity(name1, name2)

                    if name_match == True:
                        # Compute embeddings
                        embedding1 = image_to_embedding(img1, model, preprocess)
                        embedding2 = image_to_embedding(img2, model, preprocess)

                        # Calculate similarity
                        similarity_raw = calculate_cosine_similarity(embedding1, embedding2)
                        similarity_percent = similarity_raw * 100

                        # Write to CSV
                        writer.writerow([img1.name, img2.name, round(similarity_raw, 4), round(similarity_percent, 2)])
                        matched = True
                        break
                if matched == False:
                    writer.writerow([img1.name, 'Not found', 0, 0])

        print(f"Similarity results saved to: {output_csv}")



def generate_and_save_matplotagent_similarity_scores(input_dir1, input_dir2, target_dir):
    input_dir1 = Path(input_dir1)
    # input_dir2 = Path(input_dir2)
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Find all PNG images
    images1 = list(input_dir1.glob('*.png'))
    # images2 = list(input_dir2.glob('*.png'))

    # Load a pretrained model for feature extraction
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Identity()  # Remove final classification layer
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    for iteration in range(0, 7):
        output_csv = target_dir / f'similarity_results_{iteration}.csv'
        input_dir2_iteration = input_dir2+'_'+str(iteration)
        input_dir2_iteration = Path(input_dir2_iteration)
        images2 = list(input_dir2_iteration.glob('*.png'))

        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Base Image', 'Generated Image', 'Similarity Raw', 'Similarity (%)'])

            for img1 in images1:
                name1 = img1.stem.lower()

                matched = False
                for img2 in images2:
                    name2 = img2.stem.lower()
                    name_match = get_id_similarity(name1, name2)

                    if name_match == True:
                        # Compute embeddings
                        embedding1 = image_to_embedding(img1, model, preprocess)
                        embedding2 = image_to_embedding(img2, model, preprocess)

                        # Calculate similarity
                        similarity_raw = calculate_cosine_similarity(embedding1, embedding2)
                        similarity_percent = similarity_raw * 100

                        # Write to CSV
                        writer.writerow([img1.name, img2.name, round(similarity_raw, 4), round(similarity_percent, 2)])
                        matched = True
                        break
                if matched == False:
                    writer.writerow([img1.name, 'Not found', 0, 0])

        print(f"Similarity results saved to: {output_csv}")

def generate_and_save_iterative_climate_CLIP_similarity_scores(input_dir1, input_dir2, target_dir):
    input_dir1 = Path(input_dir1)
    # input_dir2 = Path(input_dir2)
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Find all PNG images
    images1 = list(input_dir1.glob('*.png'))
    # images2 = list(input_dir2.glob('*.png'))

    # Load a pretrained model for feature extraction
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Identity()  # Remove final classification layer
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    for iteration in range(0, 7):
        output_csv = target_dir / f'similarity_results_{iteration}.csv'
        input_dir2_iteration = input_dir2+'_'+str(iteration)
        input_dir2_iteration = Path(input_dir2_iteration)
        images2 = list(input_dir2_iteration.glob('*.png'))

        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Base Image', 'Generated Image', 'Similarity Raw', 'Similarity (%)'])

            for img1 in images1:
                name1 = img1.stem.lower()

                matched = False
                for img2 in images2:
                    name2 = img2.stem.lower()
                    name_match = get_name_similarity(name1, name2)

                    if name_match >=0.5:
                        # Compute embeddings
                        embedding1 = image_to_embedding(img1, model, preprocess)
                        embedding2 = image_to_embedding(img2, model, preprocess)

                        # Calculate similarity
                        similarity_raw = calculate_cosine_similarity(embedding1, embedding2)
                        similarity_percent = similarity_raw * 100

                        # Write to CSV
                        writer.writerow([img1.name, img2.name, round(similarity_raw, 4), round(similarity_percent, 2)])
                        matched = True
                        break
                if matched == False:
                    writer.writerow([img1.name, 'Not found', 0, 0])

        print(f"Similarity results saved to: {output_csv}")

from skimage.metrics import structural_similarity as ssim
import cv2

def generate_and_save_iterative_matplotagent_structural_similarity_scores(input_dir1, input_dir2, target_dir):
    input_dir1 = Path(input_dir1)
    # input_dir2 = Path(input_dir2)
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Find all PNG images
    images1 = list(input_dir1.glob('*.png'))
    print(f'Base images: {len(images1)}')
    images1 = sorted(images1)
    
    # images1 = images1.sort()
    # images2 = list(input_dir2.glob('*.png'))

    # Load a pretrained model for feature extraction
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Identity()  # Remove final classification layer
    model.eval()

    # preprocess = transforms.Compose([
    #     transforms.Resize((224, 224)),
    #     transforms.ToTensor(),
    #     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    # ])

    for iteration in range(0, 7):
        output_csv = target_dir / f'similarity_results_{iteration}.csv'
        input_dir2_iteration = input_dir2+'_'+str(iteration)
        input_dir2_iteration = Path(input_dir2_iteration)
        images2 = list(input_dir2_iteration.glob('*.png'))

        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Base Image', 'Generated Image', 'Similarity Raw', 'Similarity (%)'])

            for img1 in images1:
                # name1 = img1.stem.lower()
                name1 = img1.stem

                matched = False
                for img2 in images2:
                    # name2 = img2.stem.lower()
                    name2 = img2.stem
                    name_match = get_id_similarity(name1, name2)

                    if name_match == True:
                        # Compute embeddings
                        # embedding1 = image_to_embedding(img1, model, preprocess)
                        # embedding2 = image_to_embedding(img2, model, preprocess)
                        img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
                        img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
                        
                        # Resize generated image to match ground truth dimensions
                        img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))  # (width, height)

                        # score, _ = ssim(img1, img2, full=True)
                        score, _ = ssim(img1, img2_resized, full=True)
                        print("SSIM score:", score)
                        similarity_raw = score

                        # Calculate similarity
                        # similarity_raw = calculate_cosine_similarity(embedding1, embedding2)
                        similarity_percent = similarity_raw * 100

                        # Write to CSV
                        # writer.writerow([img1.name, img2.name, round(similarity_raw, 4), round(similarity_percent, 2)])
                        writer.writerow([name1, name2, round(similarity_raw, 4), round(similarity_percent, 2)])
                        matched = True
                        break
                if matched == False:
                    writer.writerow([name1, 'Not found', 0, 0])

        print(f"Similarity results saved to: {output_csv}")

def generate_and_save_iterative_climate_structural_similarity_scores(input_dir1, input_dir2, target_dir):
    input_dir1 = Path(input_dir1)
    # input_dir2 = Path(input_dir2)
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Find all PNG images
    images1 = list(input_dir1.glob('*.png'))
    print(f'Base images: {len(images1)}')
    images1 = sorted(images1)
    
    # images1 = images1.sort()
    # images2 = list(input_dir2.glob('*.png'))

    # Load a pretrained model for feature extraction
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Identity()  # Remove final classification layer
    model.eval()

    # preprocess = transforms.Compose([
    #     transforms.Resize((224, 224)),
    #     transforms.ToTensor(),
    #     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    # ])

    for iteration in range(0, 7):
        output_csv = target_dir / f'similarity_results_{iteration}.csv'
        input_dir2_iteration = input_dir2+'_'+str(iteration)
        input_dir2_iteration = Path(input_dir2_iteration)
        images2 = list(input_dir2_iteration.glob('*.png'))

        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Base Image', 'Generated Image', 'Similarity Raw', 'Similarity (%)'])

            for img1 in images1:
                # name1 = img1.stem.lower()
                name1 = img1.stem

                matched = False
                for img2 in images2:
                    # name2 = img2.stem.lower()
                    name2 = img2.stem
                    name_match = get_name_similarity(name1, name2)

                    if name_match >= 0.5:
                        # Compute embeddings
                        # embedding1 = image_to_embedding(img1, model, preprocess)
                        # embedding2 = image_to_embedding(img2, model, preprocess)
                        img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
                        img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
                        
                        # Resize generated image to match ground truth dimensions
                        img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))  # (width, height)

                        # score, _ = ssim(img1, img2, full=True)
                        score, _ = ssim(img1, img2_resized, full=True)
                        print("SSIM score:", score)
                        similarity_raw = score

                        # Calculate similarity
                        # similarity_raw = calculate_cosine_similarity(embedding1, embedding2)
                        similarity_percent = similarity_raw * 100

                        # Write to CSV
                        # writer.writerow([img1.name, img2.name, round(similarity_raw, 4), round(similarity_percent, 2)])
                        writer.writerow([name1, name2, round(similarity_raw, 4), round(similarity_percent, 2)])
                        matched = True
                        break
                if matched == False:
                    writer.writerow([name1, 'Not found', 0, 0])

        print(f"Similarity results saved to: {output_csv}")

def generate_and_save_climate_CLIP_similarity_scores(input_dir1, input_dir2, target_dir):
    input_dir1 = Path(input_dir1)
    # input_dir2 = Path(input_dir2)
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Find all PNG images
    images1 = list(input_dir1.glob('*.png'))
    print(f'Base images: {len(images1)}')
    images1 = sorted(images1)
    
    # images1 = images1.sort()
    # images2 = list(input_dir2.glob('*.png'))

    # Load a pretrained model for feature extraction
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Identity()  # Remove final classification layer
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # for iteration in range(0, 7):
    output_csv = target_dir / f'similarity_results_.csv'
    input_dir2_iteration = input_dir2
    input_dir2_iteration = Path(input_dir2_iteration)
    images2 = list(input_dir2_iteration.glob('*.png'))

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Base Image', 'Generated Image', 'Similarity Raw', 'Similarity (%)'])

        for img1 in images1:
            # name1 = img1.stem.lower()
            name1 = img1.stem

            matched = False
            for img2 in images2:
                # name2 = img2.stem.lower()
                name2 = img2.stem
                name_match = get_name_similarity(name1, name2)

                if name_match >= 0.5:
                    # Compute embeddings
                    embedding1 = image_to_embedding(img1, model, preprocess)
                    embedding2 = image_to_embedding(img2, model, preprocess)
                    img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
                    img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
                    
                    # Resize generated image to match ground truth dimensions
                    # img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))  # (width, height)

                    # score, _ = ssim(img1, img2, full=True)
                    # score, _ = ssim(img1, img2_resized, full=True)
                    # print("SSIM score:", score)
                    # similarity_raw = score

                    # Calculate similarity
                    similarity_raw = calculate_cosine_similarity(embedding1, embedding2)
                    similarity_percent = similarity_raw * 100

                    # Write to CSV
                    # writer.writerow([img1.name, img2.name, round(similarity_raw, 4), round(similarity_percent, 2)])
                    writer.writerow([name1, name2, round(similarity_raw, 4), round(similarity_percent, 2)])
                    matched = True
                    break
            if matched == False:
                writer.writerow([name1, 'Not found', 0, 0])

    print(f"Similarity results saved to: {output_csv}")

def generate_and_save_matplotagent_fastmribrain_CLIP_similarity_scores(input_dir1, input_dir2, target_dir):
    input_dir1 = Path(input_dir1)
    # input_dir2 = Path(input_dir2)
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Find all PNG images
    images1 = list(input_dir1.glob('*.png'))
    print(f'Base images: {len(images1)}')
    images1 = sorted(images1)
    
    # images1 = images1.sort()
    # images2 = list(input_dir2.glob('*.png'))

    # Load a pretrained model for feature extraction
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Identity()  # Remove final classification layer
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # for iteration in range(0, 7):
    output_csv = target_dir / f'similarity_results_.csv'
    input_dir2_iteration = input_dir2
    input_dir2_iteration = Path(input_dir2_iteration)
    images2 = list(input_dir2_iteration.glob('*.png'))

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Base Image', 'Generated Image', 'Similarity Raw', 'Similarity (%)'])

        for img1 in images1:
            # name1 = img1.stem.lower()
            name1 = img1.stem

            matched = False
            for img2 in images2:
                # name2 = img2.stem.lower()
                name2 = img2.stem
                name_match = get_id_similarity(name1, name2)

                if name_match == True:
                    # Compute embeddings
                    embedding1 = image_to_embedding(img1, model, preprocess)
                    embedding2 = image_to_embedding(img2, model, preprocess)
                    img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
                    img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
                    
                    # Resize generated image to match ground truth dimensions
                    # img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))  # (width, height)

                    # score, _ = ssim(img1, img2, full=True)
                    # score, _ = ssim(img1, img2_resized, full=True)
                    # print("SSIM score:", score)
                    # similarity_raw = score

                    # Calculate similarity
                    similarity_raw = calculate_cosine_similarity(embedding1, embedding2)
                    similarity_percent = similarity_raw * 100

                    # Write to CSV
                    # writer.writerow([img1.name, img2.name, round(similarity_raw, 4), round(similarity_percent, 2)])
                    writer.writerow([name1, name2, round(similarity_raw, 4), round(similarity_percent, 2)])
                    matched = True
                    break
            if matched == False:
                writer.writerow([name1, 'Not found', 0, 0])

    print(f"Similarity results saved to: {output_csv}")

import sys

if __name__ == '__main__':
    # Check if argument is passed
    
    # operation = 'process_iterative_climate_images'
    # operation = 'process_iterative_matplotagent_images'
    operation = 'process_iterative_fastmribrain_images'
    
    
    # operation = 'process_non_iterative_climate_images'
    # operation = 'process_non_iterative_matplotagent_images'
    # operation = 'process_non_iterative_fastmribrain_images'
    
    # if len(sys.argv) > 1:
    #     operation = sys.argv[1]
    #     print(f"Operation: {operation}!")
    # else:
    #     print("No argument passed.")

    project_base_directory = "/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data"
    data_base_directory = "/Users/apukumarchakroborti/gsu_research/llam_test"   
    
    # ----------------------------------------------ITERATIVE CLIMATE START--------------------------------
    # process fastmribrain images
    if operation == 'process_iterative_climate_images':
        list_of_python_scripts_sub_dirs_for_climate = [
            "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_corrector",
            "devstral_24b_climate_iterative_error_resolve_python_scripts_with_rag_with_errors_with_corrector"
            ]
        input_dir1 = f'{project_base_directory}/evaluation_by_clip_algorithm/climate_base_images'
        common_path = f"{project_base_directory}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/generated_image_from_running_evaluation"
        target_sub_dir = '/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'
        
        for index in range(0, 2):
            # images from python script evaluation
            input_dir2 = common_path+'/'+list_of_python_scripts_sub_dirs_for_climate[index]
            
            # the similarity score result will be stored here
            target_dir = project_base_directory+'/'+target_sub_dir+'/'+list_of_python_scripts_sub_dirs_for_climate[index]
            # CLIP
            generate_and_save_iterative_climate_CLIP_similarity_scores(input_dir1, input_dir2, target_dir)

            # cv2
            # generate_and_save_iterative_climate_structural_similarity_scores(input_dir1, input_dir2, target_dir) 
            # 
    # ----------------------------------------------ITERATIVE CLIMATE END--------------------------------

    # ----------------------------------------------ITERATIVE MATPLOTAGENT START--------------------------------
    # process matplotagent images
    if operation == 'process_iterative_matplotagent_images':

        list_of_python_scripts_sub_dirs_for_matplotagent = [
            "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_corrector",
            "devstral_24b_matplotagent_iterative_python_scripts_with_rag_with_errors_with_corrector"
            ]

        input_dir1 = f'{project_base_directory}/evaluation_by_clip_algorithm/matplotagent_base_images'
        common_path = f"{project_base_directory}/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve/generated_image_from_running_evaluation"
        target_sub_dir = '/matplot_agent_data/plot_generation/error_categorization_evaluation_result/iterative_error_resolve'
        
        for index in range(0, 2):
            # images from python script evaluation
            input_dir2 = common_path+'/'+list_of_python_scripts_sub_dirs_for_matplotagent[index]
            
            # the similarity score result will be stored here
            target_dir = project_base_directory+'/'+target_sub_dir+'/'+list_of_python_scripts_sub_dirs_for_matplotagent[index]
            # CLIP
            generate_and_save_iterative_matplotagent_fastmribrain_similarity_scores(input_dir1, input_dir2, target_dir)
            # cv2
            # generate_and_save_iterative_matplotagent_structural_similarity_scores(input_dir1, input_dir2, target_dir) 

    # ----------------------------------------------ITERATIVE MATPLOTAGENT END--------------------------------

    # ----------------------------------------------ITERATIVE FASTMRIBRAIN START--------------------------------
    # process fastmribrain images
    if operation == 'process_iterative_fastmribrain_images':
        list_of_python_scripts_sub_dirs_for_fastmribrain = [
            "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_corrector",
            "devstral_24b_fastmribrain_iterative_python_scripts_with_rag_with_errors_with_corrector"
            ]

        input_dir1 = f'{project_base_directory}/evaluation_by_clip_algorithm/fastmribrain_base_images'
        common_path = f"{project_base_directory}/mri_nyu_data/error_categorization_evaluation_result/iterative_evaluation_results/generated_image_from_running_evaluation"
        target_sub_dir = '/mri_nyu_data/error_categorization_evaluation_result/iterative_evaluation_results'
        
        for index in range(0, 2):
            # images from python script evaluation
            input_dir2 = common_path+'/'+list_of_python_scripts_sub_dirs_for_fastmribrain[index]
            
            # the similarity score result will be stored here
            target_dir = project_base_directory+'/'+target_sub_dir+'/'+list_of_python_scripts_sub_dirs_for_fastmribrain[index]
            # CLIP
            generate_and_save_iterative_matplotagent_fastmribrain_similarity_scores(input_dir1, input_dir2, target_dir)

            # cv2
            # generate_and_save_iterative_matplotagent_structural_similarity_scores(input_dir1, input_dir2, target_dir) 
    # ----------------------------------------------ITERATIVE FASTMRIBRAIN END--------------------------------

    # ----------------------------------------------NON-ITERATIVE CLIMATE START--------------------------------
    # generate_and_save_matplotagent_similarity_scores
    if operation == 'process_non_iterative_climate_images':
        # simple vs expert queries
        list_of_python_scripts_sub_dirs_for_climate = [
            "deepseek_r1_32b_python_scripts_without_rag_with_errors_without_corrector",
            "deepseek_r1_32b_python_scripts_without_rag_without_corrector",

            "devstral_24b_python_scripts_without_rag_with_errors_without_corrector",
            "devstral_24b_python_scripts_without_rag_without_corrector",

            "llama3_70b_python_scripts_without_rag_with_errors_without_corrector",
            "llama3_70b_python_scripts_without_rag_without_corrector",

            "magicoder_python_scripts_without_rag_with_errors_without_corrector",
            "magicoder_python_scripts_without_rag_without_corrector",

            "gemma3_27b_python_scripts_without_rag_with_errors_without_corrector",
            "gemma3_27b_python_scripts_without_rag_without_corrector",

            # for the corrector without corrector
            "devstral_24b_python_scripts_without_rag_with_errors_without_corrector",
            "devstral_24b_python_scripts_without_rag_with_errors_with_corrector",

            "magicoder_python_scripts_without_rag_with_errors_without_corrector",
            "magicoder_python_scripts_without_rag_with_errors_with_corrector",

            "llama3_70b_python_scripts_without_rag_with_errors_without_corrector",
            "llama3_70b_python_scripts_without_rag_with_errors_with_corrector",

            "gemma3_27b_python_scripts_without_rag_with_errors_without_corrector",
            "gemma3_27b_python_scripts_without_rag_with_errors_with_corrector",
            
            "deepseek_r1_32b_python_scripts_without_rag_with_errors_without_corrector",
            "deepseek_r1_32b_python_scripts_without_rag_with_errors_with_corrector",

            # with corrector enabled and with and without rag
            "devstral_24b_python_scripts_without_rag_with_errors_with_corrector",
            "devstral_24b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",

            "magicoder_python_scripts_without_rag_with_errors_with_corrector",
            "magicoder_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",

            "llama3_70b_python_scripts_without_rag_with_errors_with_corrector",
            "llama3_70b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",

            "gemma3_27b_python_scripts_without_rag_with_errors_with_corrector",
            "gemma3_27b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",
            
            "deepseek_r1_32b_python_scripts_without_rag_with_errors_with_corrector",
            "deepseek_r1_32b_python_scripts_with_rag_multi_agents_and_sub_query_decomposition_with_errors_with_corrector",
            

            ]
        input_dir1 = f'{project_base_directory}/evaluation_by_clip_algorithm/climate_base_images'
        common_path = f"{project_base_directory}/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag/generated_image_from_running_evaluation/without_iterative_process"
        
        target_sub_dir = '/prompting_techniques/zero_shot_sci_data_prompting/error_categorization_evaluation_result/llm_generated_code_with_rag'
        
        for index in range(20, 30):
            # images from python script evaluation
            input_dir2 = common_path+'/'+list_of_python_scripts_sub_dirs_for_climate[index]
            
            # the similarity score result will be stored here
            target_dir = project_base_directory+'/'+target_sub_dir+'/'+list_of_python_scripts_sub_dirs_for_climate[index]
            # CLIP
            generate_and_save_climate_CLIP_similarity_scores(input_dir1, input_dir2, target_dir)
    # ----------------------------------------------NON-ITERATIVE CLIMATE END--------------------------------
    
    # ----------------------------------------------NON-ITERATIVE MATPLOTAGENT START--------------------------------
    if operation == 'process_non_iterative_matplotagent_images':
        # simple vs expert queries
        list_of_python_scripts_sub_dirs_for_matplotagent = [
            #simple vs expert    
            "deepseek_r1_32b_matplotagent_python_scripts_without_rag_with_errors_without_corrector",
            "deepseek_r1_32b_matplotagent_python_scripts_without_rag_without_corrector",

            "devstral_24b_matplotagent_python_scripts_without_rag_with_errors_without_corrector",
            "devstral_24b_matplotagent_python_scripts_without_rag_without_corrector",
            

            "llama3_70b_matplotagent_python_scripts_without_rag_with_errors_without_corrector",
            "llama3_70b_matplotagent_python_scripts_without_rag_without_corrector",
            
            "magicoder_matplotagent_python_scripts_without_rag_with_errors_without_corrector",
            "magicoder_matplotagent_python_scripts_without_rag_without_corrector",

            "gemma3_27b_matplotagent_python_scripts_without_rag_with_errors_without_corrector",
            "gemma3_27b_matplotagent_python_scripts_without_rag_without_corrector",

            #simple query with and without corrector
            "devstral_24b_matplotagent_python_scripts_without_rag_with_errors_without_corrector",
            "devstral_24b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",

            "magicoder_matplotagent_python_scripts_without_rag_with_errors_without_corrector",
            "magicoder_matplotagent_python_scripts_without_rag_with_errors_with_corrector",            

            "llama3_70b_matplotagent_python_scripts_without_rag_with_errors_without_corrector",
            "llama3_70b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",     
            
            "gemma3_27b_matplotagent_python_scripts_without_rag_with_errors_without_corrector",
            "gemma3_27b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",

            "deepseek_r1_32b_matplotagent_python_scripts_without_rag_with_errors_without_corrector",
            "deepseek_r1_32b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",

            #simple query with corrector and with and without rag  
            "devstral_24b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",
            "devstral_24b_matplotagent_python_scripts_with_rag_with_errors_with_corrector",

            "magicoder_matplotagent_python_scripts_without_rag_with_errors_with_corrector",
            "magicoder_matplotagent_python_scripts_with_rag_with_errors_with_corrector",
            
            "llama3_70b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",
            "llama3_70b_matplotagent_python_scripts_with_rag_with_errors_with_corrector",
            
            "gemma3_27b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",
            "gemma3_27b_matplotagent_python_scripts_with_rag_with_errors_with_corrector",

            "deepseek_r1_32b_matplotagent_python_scripts_without_rag_with_errors_with_corrector",
            "deepseek_r1_32b_matplotagent_python_scripts_with_rag_with_errors_with_corrector",
  
            ]
        input_dir1 = f'{project_base_directory}/evaluation_by_clip_algorithm/matplotagent_base_images'
        common_path = f"{project_base_directory}/matplot_agent_data/plot_generation/error_categorization_evaluation_result/generated_image_from_running_evaluation"
        
        target_sub_dir = '/matplot_agent_data/plot_generation/error_categorization_evaluation_result/llm_generated_code_with_rag'
        
        for index in range(10, 30):
            # images from python script evaluation
            input_dir2 = common_path+'/'+list_of_python_scripts_sub_dirs_for_matplotagent[index]
            
            # the similarity score result will be stored here
            target_dir = project_base_directory+'/'+target_sub_dir+'/'+list_of_python_scripts_sub_dirs_for_matplotagent[index]
            # CLIP
            generate_and_save_matplotagent_fastmribrain_CLIP_similarity_scores(input_dir1, input_dir2, target_dir)
    # ----------------------------------------------NON-ITERATIVE MATPLOTAGENT END--------------------------------

    # ----------------------------------------------NON-ITERATIVE FASTMRIBRAIN START--------------------------------
    if operation == 'process_non_iterative_fastmribrain_images':
        # simple vs expert queries
        list_of_python_scripts_sub_dirs_for_climate = [
            

            "devstral_24b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector",
            "devstral_24b_fastmribrain_python_scripts_without_rag_without_corrector",

            "magicoder_fastmribrain_python_scripts_without_rag_with_errors_without_corrector",
            "magicoder_fastmribrain_python_scripts_without_rag_without_corrector",

            "llama3_70b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector",
            "llama3_70b_fastmribrain_python_scripts_without_rag_without_corrector",

            "gemma3_27b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector",
            "gemma3_27b_fastmribrain_python_scripts_without_rag_without_corrector",

            "deepseek_r1_32b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector",
            "deepseek_r1_32b_fastmribrain_python_scripts_without_rag_without_corrector", 

            # simple query with and without corrector
            "devstral_24b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector",
            "devstral_24b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",

            "magicoder_fastmribrain_python_scripts_without_rag_with_errors_without_corrector",
            "magicoder_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",

            "llama3_70b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector",
            "llama3_70b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",

            "gemma3_27b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector",
            "gemma3_27b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",

            "deepseek_r1_32b_fastmribrain_python_scripts_without_rag_with_errors_without_corrector",
            "deepseek_r1_32b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector", 

            #simple query with corrector and with and without rag
            "devstral_24b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",
            "devstral_24b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector",

            "magicoder_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",
            "magicoder_fastmribrain_python_scripts_with_rag_with_errors_with_corrector",

            "llama3_70b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",
            "llama3_70b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector",

            "gemma3_27b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",
            "gemma3_27b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector",

            "deepseek_r1_32b_fastmribrain_python_scripts_without_rag_with_errors_with_corrector",
            "deepseek_r1_32b_fastmribrain_python_scripts_with_rag_with_errors_with_corrector",  
            ]
        input_dir1 = f'{project_base_directory}/evaluation_by_clip_algorithm/fastmribrain_base_images'
        common_path = f"{project_base_directory}/mri_nyu_data/error_categorization_evaluation_result/non_iterative_evaluation_results/fastmribrain"
        
        target_sub_dir = '/mri_nyu_data/error_categorization_evaluation_result/llm_generated_code_with_rag'
        
        for index in range(10, 30):
            # images from python script evaluation
            input_dir2 = common_path+'/'+list_of_python_scripts_sub_dirs_for_climate[index]
            
            # the similarity score result will be stored here
            target_dir = project_base_directory+'/'+target_sub_dir+'/'+list_of_python_scripts_sub_dirs_for_climate[index]
            # CLIP
            generate_and_save_matplotagent_fastmribrain_CLIP_similarity_scores(input_dir1, input_dir2, target_dir)
    # ----------------------------------------------NON-ITERATIVE FASTMRIBRAIN END--------------------------------
    
  
    if operation == 'process_scripts':
        list_of_python_scripts_sub_dirs = ["deepseek_r1_70b_F_IQR_generated_python_scripts_from_simple_user_queries_final", #0
                                        "deepseek_r1_70b_Z_SCORE_generated_python_scripts_from_simple_user_queries_final", #1
                                        "deepseek_r1_70b_IQR_generated_python_scripts_from_simple_user_queries_final", #2
                                        "deepseek_r1_70b_generated_python_scripts_from_expert_queries_final", #3
                                        "deepseek_r1_70b_generated_python_scripts_from_simple_queries_final", #4

                                        "llama3_70b_F_IQR_generated_python_scripts_from_simple_user_queries_final", #5
                                        "llama3_70b_Z_SCORE_generated_python_scripts_from_simple_user_queries_final", #6
                                        "llama3_70b_IQR_generated_python_scripts_from_simple_user_queries_final", #7
                                        "llama3_70b_generated_python_scripts_from_expert_queries_final", #8
                                        "llama3_70b_generated_python_scripts_from_simple_queries_final", #9

                                        "magicoder_F_IQR_generated_python_scripts_from_simple_user_queries_final", #10
                                        "magicoder_Z_SCORE_generated_python_scripts_from_simple_user_queries_final", #11
                                        "magicoder_IQR_generated_python_scripts_from_simple_user_queries_final", #12
                                        "magicoder_generated_python_scripts_from_expert_queries_final", #13
                                        "magicoder_generated_python_scripts_from_simple_queries_final", #14

                                        "deepseek_r1_70b_generated_python_scripts_from_llms_modified_expert_queries_final", #15
                                        "llama3_70b_generated_python_scripts_from_llms_modified_expert_queries_final", #16
                                        "magicoder_generated_python_scripts_from_llms_modified_expert_queries_final" #17
                                        ]
        common_path = project_base_directory+"/llms_generated_python_scripts"        

        # collect and store all images
        subdirectories = [f'{data_base_directory}/ACL_DIRS/ASF',
                            f'{data_base_directory}/ACL_DIRS/AURA_DATA_VC',
                            f'{data_base_directory}/ACL_DIRS/GES_DISC',
                            f'{data_base_directory}/ACL_DIRS/ICESat_2',
                            f'{data_base_directory}/ACL_DIRS/LAADS',
                            f'{data_base_directory}/ACL_DIRS/LaRC',
                            f'{data_base_directory}/ACL_DIRS/LP_DAAC',
                            f'{data_base_directory}/ACL_DIRS/NSIDC',
                            f'{data_base_directory}/ACL_DIRS/PO_DAAC',
                            f'{data_base_directory}',
                            f'{project_base_directory}/automatic_outliers_detection_for_scientific_data_visualization',
                            f'{project_base_directory}'
                        ]
        for index in range(0, 15):
            python_scripts_directory = common_path+"/"+list_of_python_scripts_sub_dirs[index]
            execute_python_scripts(python_scripts_directory)            
            source_dirs = subdirectories  # List of source directories
            target_dir = f"{project_base_directory}/generated_images_from_experiments/"+list_of_python_scripts_sub_dirs[index]
            collect_and_store_png(source_dirs, target_dir)
    elif operation == 'process_images':
        list_of_python_scripts_sub_dirs = ["deepseek_r1_70b_F_IQR_generated_python_scripts_from_simple_user_queries_final", #0
                                        "deepseek_r1_70b_Z_SCORE_generated_python_scripts_from_simple_user_queries_final", #1
                                        "deepseek_r1_70b_IQR_generated_python_scripts_from_simple_user_queries_final", #2
                                        "deepseek_r1_70b_generated_python_scripts_from_expert_queries_final", #3
                                        "deepseek_r1_70b_generated_python_scripts_from_simple_queries_final", #4

                                        "llama3_70b_F_IQR_generated_python_scripts_from_simple_user_queries_final", #5
                                        "llama3_70b_Z_SCORE_generated_python_scripts_from_simple_user_queries_final", #6
                                        "llama3_70b_IQR_generated_python_scripts_from_simple_user_queries_final", #7
                                        "llama3_70b_generated_python_scripts_from_expert_queries_final", #8
                                        "llama3_70b_generated_python_scripts_from_simple_queries_final", #9

                                        "magicoder_F_IQR_generated_python_scripts_from_simple_user_queries_final", #10
                                        "magicoder_Z_SCORE_generated_python_scripts_from_simple_user_queries_final", #11
                                        "magicoder_IQR_generated_python_scripts_from_simple_user_queries_final", #12
                                        "magicoder_generated_python_scripts_from_expert_queries_final", #13
                                        "magicoder_generated_python_scripts_from_simple_queries_final", #14

                                        "deepseek_r1_70b_generated_python_scripts_from_llms_modified_expert_queries_final", #15
                                        "llama3_70b_generated_python_scripts_from_llms_modified_expert_queries_final", #16
                                        "magicoder_generated_python_scripts_from_llms_modified_expert_queries_final" #17
                                        ]
        input_dir1 = f'{project_base_directory}/base_images'
        common_path = f"{project_base_directory}/generated_images_from_experiments"
        
        for index in range(0, 15):
            input_dir2 = common_path+'/'+list_of_python_scripts_sub_dirs[index]
            target_dir = common_path+'/similarity_score_files/'+list_of_python_scripts_sub_dirs[index]

            generate_and_save_similarity_scores(input_dir1, input_dir2, target_dir) 