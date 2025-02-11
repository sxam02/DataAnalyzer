# Data Whisperer

Data Whisperer is an interactive data analysis platform built with Streamlit and Pandas. It allows users to upload Excel files, ask questions about their data in natural language, and visualize the results.

## Features

- Upload Excel files for analysis.
- Ask questions about your data using natural language.
- View data summaries and visualizations.
- Export results to Excel.

## Requirements

- Python 3.9 or higher
- Streamlit
- Pandas
- OpenAI
- OpenPyXL
- PandasAI
- Plotly
- PyYAML
- xlrd
- pdfkit (optional, if PDF export is included)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/data-whisperer.git
   cd data-whisperer
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, if you are using `pyproject.toml`, you can install dependencies using:

   ```bash
   pip install .
   ```

4. Install `wkhtmltopdf` for PDF export (if applicable):

   - **For Ubuntu/Debian**:
     ```bash
     sudo apt-get install wkhtmltopdf
     ```

   - **For macOS**:
     ```bash
     brew install wkhtmltopdf
     ```

   - **For Windows**:
     Download the installer from [wkhtmltopdf releases page](https://github.com/wkhtmltopdf/packaging/releases) and follow the installation instructions.

## Usage

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501` (or the port specified in the command).

3. Upload your Excel file and start asking questions about your data!

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [OpenAI](https://openai.com/)
- [DuckDB](https://duckdb.org/)