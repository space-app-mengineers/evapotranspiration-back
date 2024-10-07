# Labkence EvapoTranspiration Analyzer

We present Labkence, a disruptive platform that utilizes NASA’s satellite data at the service of smallholder farmers, specially in Chile. This way, Labkence will empower them to take critical water-related decisions informed with real data. Our platform not only delivers key metrics to farmers but also translates this data into simple, manageable insights tailored to general information about the farmer's land and resources. 

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Jupyter Notebook](#running-the-jupyter-notebook)
  - [FastAPI](#running-the-fastapi-app)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Set up a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Jupyter Notebook

1. Start the Jupyter Notebook server:

    ```bash
    jupyter notebook
    ```

2. Open the `ET_processing.ipynb` file from the Jupyter interface.

### Running the FastAPI App

1. To start the FastAPI app, run the following command:

    ```bash
    uvicorn app:app --reload
    ```

    This assumes that your FastAPI application is defined in a file named `app.py` with an instance called `app`.

2. Access the FastAPI app at `http://127.0.0.1:8000`.

3. You can view the automatically generated API docs at:

    - Swagger UI: `http://127.0.0.1:8000/docs`
    - Redoc: `http://127.0.0.1:8000/redoc`

## Requirements

All dependencies are listed in the `requirements.txt` file. You can install them using the following command:

```bash
pip install -r requirements.txt
```
