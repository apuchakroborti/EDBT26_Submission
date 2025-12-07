"""
To read and examine the data structures and data from a DICOM (`.dcm`) file in Python, you can use the **pydicom** library. This library is specifically designed for parsing, modifying, and extracting information from DICOM files. Below is a step-by-step explanation and example:

---

### 1. **Install Required Libraries**
Ensure you have the `pydicom` library installed:
```bash
pip install pydicom
```

---

### 2. **Read a DICOM File**
Use the `pydicom.dcmread()` function to load the DICOM file.

```python

"""
import pydicom

# Path to your DICOM file
dicom_file = "/Users/apukumarchakroborti/gsu_research/llam_test/mri_nyu_data/DICOMS/001/AX_DIFFUSION_ADC/96.dcm"

# Read the DICOM file
dicom_data = pydicom.dcmread(dicom_file)
"""
```

---

### 3. **Examine Data Structures**
The `dicom_data` object contains metadata and pixel data. Here’s how you can inspect it:

#### a) **View Metadata**
To see the structure of the file and its attributes:
```python
"""
# Print a summary of the file
print('-------------Print a summary of the file----------------')
# print(dicom_data)
# List all available tags
print('\n\n-------------List all available tags-----------------')
print(dicom_data.dir())
"""
```

#### b) **Access Specific Attributes**
You can query metadata by its name or DICOM tag:
```python
"""
# Patient Information
print("Patient Name:", dicom_data.PatientName)
print("Patient ID:", dicom_data.PatientID)

# Imaging Details
print("Modality:", dicom_data.Modality)
print("Study Date:", dicom_data.StudyDate)

# Access using DICOM tag numbers
print('\n\n----------------------Access using DICOM tag numbers---------------------------')
print("Slice Thickness:", dicom_data[0x0018, 0x0050].value)  # (0018, 0050) is the tag for Slice Thickness

"""
```

#### c) **Iterate Over All Metadata**
You can iterate through all tags and their values:
```python
"""

# for element in dicom_data:
    # print(f"{element.tag} {element.name}: {element.value}")

"""
```

---

### 4. **Extract and Visualize Pixel Data**
The pixel data contains the actual image in raw or encoded form.

```python
"""
import matplotlib.pyplot as plt
import numpy as np

# Extract pixel array
pixel_array = dicom_data.pixel_array

# Print pixel array shape
print('\n\n-------------------Print pixel array shape----------------------')
print("Pixel Data Shape:", pixel_array.shape)

# Display the image
# plt.imshow(pixel_array, cmap='gray')
# plt.title("DICOM Image")
# plt.colorbar()
# plt.show()

"""
```

---

### 5. **Advanced Analysis**
#### a) **Inspect Pixel Data Details**
To better understand the encoding of the pixel data:
```python

"""
print('\n\n------------Inspect Pixel Data Details------------')
print("Bits Allocated:", dicom_data.BitsAllocated)
print("Bits Stored:", dicom_data.BitsStored)
print("High Bit:", dicom_data.HighBit)
print("Pixel Representation:", dicom_data.PixelRepresentation)

"""
```

#### b) **Check Compression (Transfer Syntax)**
Some DICOM files are compressed; you can check the transfer syntax:
```python
print("Transfer Syntax UID:", dicom_data.file_meta.TransferSyntaxUID)
```

---

### 6. **Full Summary of Metadata and Pixel Data**
Here’s a concise way to explore everything in the file:
```python
"""

# Print full metadata
print('\n\n--------------------Print full metadata---------------------')
print(dicom_data)

# Print pixel array statistics
pixel_array = dicom_data.pixel_array
print("\n\n---------------Pixel Array Statistics:------------------")
print("Min:", np.min(pixel_array))
print("Max:", np.max(pixel_array))
print("Mean:", np.mean(pixel_array))

"""
```

---

### Example Output
For a typical DICOM file:
1. **Metadata**:
   ```
   (0010, 0010) Patient's Name: John Doe
   (0020, 000d) Study Instance UID: 1.2.840.113619.2.1.2411.1031152385
   (0008, 0060) Modality: CT
   ```
2. **Pixel Array**:
   ```
   Pixel Array Shape: (512, 512)
   Min: 0, Max: 4096, Mean: 512.8
   ```

---

### Tools for Validation and Exploration
- **DICOM Viewers**:
  Tools like *Horos*, *OsiriX*, or *3D Slicer* can help validate and explore the DICOM files visually.
- **HDF5 Conversion**:
  If working with large datasets, converting DICOM files to HDF5 format (as shown earlier) can streamline data management.

Let me know if you need help with a specific file or visualization technique!
"""