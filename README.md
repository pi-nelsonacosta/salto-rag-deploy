## Contents
[RAG Model](#rag-model-robot)<br>
- [Overview](#mag-overview)<br>
- [Components](#open_file_folder-components)<br>
- [Tools Used](#hammer_and_wrench-tools-used)<br>
- [Getting Started](#rocket-getting-started)<br>
<!--- - [References](#books-references)<br> -->

# Simple RAG in Azure :robot:

**`........`**

## :mag: Overview
......

## :open_file_folder: Components
Below is a breakdown of the key components included in this repository:

- [**`config/`**](config/): Project documentation.

- [**`prompts/`**](prompts/): Test cases documentation.

- [**`services/`**](services/): Test cases documentation.

- [**`src/`**](src/): Source files for the application.
  - [`__init__.py`](src/__init__.py): Initializes src as a Python module.
  - [`main.py`](src/main.py): Main script to run the application.
  - [`app.py`](src/app.py): Flask application endpoints.
  - [`rag_model.py`](src/rag_model.py): RAG Model functionality and methods.

- [**`requirements.txt`**](requirements.txt): Python dependencies.

- [**`.gitignore`**](.gitignore): Specifies intentionally untracked files to ignore.

- [**`README.md`**](README.md): Detailed description of the project.

- [**`LICENSE`**](LICENSE): MIT License information.


## :hammer_and_wrench: Tools Used
The following tools are utilized in this project:

1. **LangChain**
2. **Flask**
3. **GPT-4o**
4. **ChromaDB**

## :rocket: Getting Started
Follow these steps to set up and run the project on your local machine:

1. **Clone the repository:**

``` bash
git clone https://github.com/jairzinhosantos/rag-llm-model.git
```

3. **Set up a virtual environment:**

``` bash
python -m venv venv
source venv/bin/activate
```

4. **Install dependencies:**

``` bash
pip install -r requirements.txt
```

5. **Run the application:**

``` bash
python src/main.py
```


<!---
## :books: References
[^1]: [x](y)
[^2]: [x](y)
[^3]: [x](y)
[^4]: [x](y)
-->