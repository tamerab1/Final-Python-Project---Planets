# 🪐 Planets Web Explorer - NASA Dataset Analysis

A comprehensive web application designed to explore, filter, and visualize exoplanet data from the NASA Seaborn dataset. This project demonstrates a full-stack approach to data science, combining robust backend logic with interactive frontend visualizations.

## 🚀 Key Features

* **Interactive Analytics Dashboard:** Features five specific research questions analyzing orbital periods, planetary mass, and discovery methods.
* **Dynamic Query Engine:** A custom-built filtering system that allows users to query the dataset by selecting specific columns and applying logical operators (e.g., `>`, `<`, `==`, `contains`).
* **Scientific Visualizations:** High-fidelity, interactive histograms and bar charts built with **Plotly Express**, utilizing logarithmic scales for skewed data distribution.
* **Modern Web UI:** A sleek, space-themed "Glassmorphism" interface built with **FastAPI** and **Bootstrap 5**.
* **Data Integrity & Cleaning:** Advanced preprocessing using **Pandas** to handle missing values (NaNs) and filter extreme outliers for clearer statistical insights.

## 🏗️ Architecture & OOP Design

The project follows the **Separation of Concerns (SoC)** principle, organized into a modular structure:

* **`DataService` Class:** Acts as the Data Access Layer. It implements a singleton-like pattern to load the dataset into memory once, providing efficient filtering services across the app.
* **`AnalysisService` Class:** Contains the Business Logic for statistical computations. It processes raw data into meaningful insights and generates the HTML for interactive plots.
* **Routers:** Dedicated FastAPI routers handle the request-response lifecycle, separating analysis routes from data-querying routes.
* **Jinja2 Templates:** Utilizes template inheritance to ensure a consistent UI/UX across all pages.



## 🛠️ Tech Stack

* **Backend:** FastAPI (Asynchronous Python Web Framework)
* **Data Analysis:** Pandas, NumPy
* **Visualization:** Plotly Express
* **Frontend:** Jinja2, HTML5, CSS3, Bootstrap 5
* **Version Control:** Git & GitHub

## 📂 Project Structure

```text
├── main.py              # Application entry point & configuration
├── services/            # Logic layer (DataService.py, AnalysisService.py)
├── routers/             # API Endpoints (questions.py, data.py)
├── templates/           # HTML templates using Jinja2
├── static/              # CSS styles and static assets
├── data/                # Source CSV dataset
└── .gitignore           # Git exclusion rules

🔧 Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd Final_Project_Py
Set up a Virtual Environment:

Bash
python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate
Install Dependencies:

Bash
pip install -r requirements.txt
Launch the Server:

Bash
uvicorn main:app --reload
Access the app at: http://127.0.0.1:8000
```
-----------------------------------------------------------------------------------------------------------------------------
## 📊 Sample Insights
Orbital Period Analysis: By applying a Logarithmic Scale, we successfully visualized planetary orbits ranging from 0.01 to 730,000 days, revealing that the majority of discovered planets have an orbital period between 10 and 100 days.

Mass Distribution: By filtering outliers (planets > 2 Jupiter Masses), the analysis provides a high-resolution view of Earth-like and gas-giant distributions.


## Developed as a Final Project for the Python Development Course.
