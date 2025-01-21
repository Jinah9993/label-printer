# SKU Label Generator

This application allows users to generate PDF labels for products based on data from a CSV file. The labels are designed specifically for **6x4-inch labels**, which are split into two **4x3-inch sections** per label. Users can preview the labels, adjust text dynamically, and save the PDF. The application also provides a sample CSV file with various test cases to help users get started.

![1](https://github.com/user-attachments/assets/9ac24863-eaf9-4364-95b8-ebce2a78dabf)

## Features

- **Upload CSV**: Load a CSV file containing product data for label generation.
- **Preview Labels**: Preview the generated labels before saving them to ensure correctness.
- **Dynamic Text Adjustment**: Automatically adjusts font size and wraps text to fit within the label dimensions.
- **Save Labels**: Save the generated labels as a PDF file.
- **Download Sample CSV**: Download a preconfigured sample CSV file to understand the required format and test the application.

## Requirements

- Python 3.x
- Required Python libraries:
  - `pandas`
  - `reportlab`
  - `tkinter` (built-in with Python)
  - `pdf2image`
  - `Pillow`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/sku-label-generator.git
   cd sku-label-generator
   ```

2. Install the required Python libraries:
   ```bash
   pip install pandas reportlab pdf2image Pillow
   ```

3. For Windows users, download and install [Poppler](https://github.com/oschwartz10612/poppler-windows/):
   - Add the Poppler `bin` directory to your system's PATH environment variable.

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Use the following buttons in the GUI:
   - **Upload CSV and Preview**: Select a CSV file to upload and preview the generated labels.
  ![3](https://github.com/user-attachments/assets/2d48665a-060c-435d-859d-4be0f571b5f6)
   - **Save Labels**: Save the generated labels as a PDF file.
  ![4](https://github.com/user-attachments/assets/82450b0f-1ac1-44f5-9992-a293258ab751)
   - **Download Sample CSV**: Download a sample CSV file with test cases to the `Downloads` folder.
  ![2](https://github.com/user-attachments/assets/3beabef3-7382-4971-9322-fc1f0de6b288)

## CSV Format

The uploaded CSV file should have the following columns:

| SKU          | Group               | Album                  | Item                 | Member              |
|--------------|---------------------|------------------------|----------------------|---------------------|
| LONGID012345 | SuperLongGroupName  | Extended Album Name    | Extremely Long Item  | VeryVerboseMember   |
| SHORT001     | Short               | Short Album            | Item                 | Member              |
| REGID123456  | RegularGroup        | RegularAlbum           | RegularItem          | RegularMember       |
| EDGECA789012 | EdgeCaseGroup       | EdgeAlbum              | EdgeItem             | EdgeMember          |
| MIXID654321  | MixGroup            | LongAlbumName          | ShortItem            | MixedLengthMember   |

![7](https://github.com/user-attachments/assets/ce90a4aa-16f0-4562-89f2-4bfdca6083af)

### Note on Empty Cells
If the CSV file contains empty cells, they will be displayed as `NaN` in the generated labels. To prevent this behavior, ensure all cells are filled with at least a space (`' '`).

## Preview

- The preview panel displays the first page of the generated labels.
- Each **6x4-inch label** is split into two **4x3-inch sections**, showing product information.
![5](https://github.com/user-attachments/assets/2c3316dd-cc06-4c3f-9ac0-9d9e8eea6ada)
![6](https://github.com/user-attachments/assets/018f7173-d691-4106-aa9f-a7d81dcd5b5a)

## License

This project is licensed under the MIT License.

