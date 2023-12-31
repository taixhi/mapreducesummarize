# MapReduceSummarize

MapReduceSummarize is a robust tool designed to automate the summarization of PDF documents leveraging the Map-Reduce pattern. This tool utilizes Language Models (LLMs) from OpenAI, along with the LangChain library, to efficiently process and summarize text from PDF documents. The Map-Reduce pattern facilitates parallel processing of the document, enhancing performance and scalability, especially for large PDFs.

## Features

- **PDF Processing**: Load and process PDF documents, splitting them into manageable chunks or pages.
- **Parallel Summarization**: Utilize the Map-Reduce pattern to perform parallel summarization of document chunks, improving efficiency and handling large documents with ease.
- **OpenAI Integration**: Leverage powerful language models from OpenAI to generate high-quality summaries.
- **LangChain Utilization**: Utilize LangChain for document handling, text processing, and interfacing with OpenAI.
- **Interactive UI**: An intuitive user interface built with Streamlit to upload PDFs, initiate summarization, and view results.
- **Web Accessibility**: Expose the summarization tool on the web using ngrok, making it accessible from anywhere.

## Getting Started

### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.8 or later
- pip (Python's package installer)

### Installation

1. Clone the repository to your local machine:
```bash
git clone https://github.com/taixhi/MapReduceSummarize.git
cd MapReduceSummarize
```

2. Create a virtual environment:
```bash
python -m venv env
```

3. Activate the virtual environment:
```bash
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

### Usage

1. Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY=<your_api_key>
```

2. Run the Streamlit app:
```bash
streamlit run ./app.py
```

Now, navigate to the URL provided by ngrok in a web browser to access the MapReduceSummarize app.

### License

This project is licensed under the MIT License. See the `LICENSE.md` file for details.

### Contact
Feel free to reach out to [me](https://taichikato.com) via GitHub or email for any queries or support.
