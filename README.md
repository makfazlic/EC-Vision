# EC-Vision
EC-Vision is developed for optimizing image processing across all ETH Entrepreneur Club websites. This robust pipeline enhances website efficiency by reducing image sizes by an impressive 90%, ensuring optimal performance without compromising on recommended image dimensions. Streamline your web content and elevate user experience with EC-Vision's powerful image processing capabilities.

## Demo
https://drive.google.com/file/d/1XAVGSdHCDrt69PStJNtBnT2OHeSIuK1p/view?usp=sharing

## Getting Started

### Prerequisites

- Python 3
- pip
  
### Setting Up the Environment

1. Clone the repository:
    ```
    git clone https://github.com/makfazlic/EC-Vision.git
    ```
2. Navigate to the project directory:
    ```
    cd project
    ```
3. Create a new virtual environment:
    ```
    python3 -m venv env
    ```
4. Activate the virtual environment:
    - On Windows:
        ```
        .\env\Scripts\activate
        ```
    - On Unix or MacOS:
        ```
        source env/bin/activate
        ```
5. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

## Usage


### Flags

The program supports the following flags:

- `--help`: Show the help message and exit.
- `-m MODE, --mode MODE`: MODE can be "face" or "logo" for working with portraits or logos
- `-i INPUT, --input INPUT`: INPUT can be a path to a .csv file or a folder with images


Here's a few examples of how to use the flags:
```
python run.py -m face -i ./example.csv
```
```
python run.py -m logo -i ./example.csv
```
```
python run.py -m face -i ./folder_with_images
```
