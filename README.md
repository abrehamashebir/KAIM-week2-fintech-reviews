# KAIM-week2-fintech-reviews

This repository contains a full pipeline for scraping, analyzing, and visualizing Google Play Store reviews for mobile banking apps of three major Ethiopian banks: CBE, BOA, and Dashen Bank. The goal is to uncover key insights into customer satisfaction and provide actionable recommendations for app improvement.

## 📁 Project Structure

``` bash
KAIM-week2-fintech-reviews
├── datasets
│   ├── processed
│   │   └── sentiment_theme.csv
│   └── raw
│       ├── cleaned_reviews.csv
│       └── reviews.csv
├── notebooks
│   ├── __init__.py
│   └── review_analysis.ipynb
├── plots
├── README.md
├── scripts
│   └── __init__.py
├── src
│   ├── initialize.py
│   ├── __init__.py
│   ├── preprocessor.py
│   ├── __pycache__
│   │   ├── initialize.cpython-312.pyc
│   │   ├── preprocessor.cpython-312.pyc
│   │   └── scraper.cpython-312.pyc
│   └── scraper.py
└── test
    └── __init__.py

```

## 🚀 Challenge Overview

- ✅ Scrape Google Play Store reviews
- ✅ Clean and preprocess review data
- ✅ Perform sentiment and thematic analysis using NLP
- ✅ Store data in an Oracle database
- ✅ Generate business insights and visualizations

---

## 🏦 Banks Analyzed

- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

---

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/KAIM-week2-fintech-reviews.git
    cd KAIM-week2-fintech-reviews
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Explore the notebooks in the `notebooks/` directory.

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependencies

## License

This project is licensed under the MIT License.

## Author

Abreham Ashebir

---






