# Nassau Candy Shipping Analysis

## Factory-to-Customer Shipping Route Efficiency Analysis

### Project Overview

This project analyzes shipping data from Nassau Candy Distributor to understand shipment patterns, regional sales, shipping modes, factory distribution, and geographic shipment volumes.

### Project Objectives

* Analyze shipping data using Python.
* Compare sales and shipment volumes across regions.
* Study shipping modes and factory-level distribution.
* Analyze factory-to-customer route volumes.
* Build an interactive dashboard for data exploration.

### Tools and Technologies

* Python
* Pandas
* Matplotlib
* Plotly
* Streamlit

### Dashboard Features

* Interactive filters for region, state, shipping mode, and factory.
* Sales by region and shipments by shipping mode.
* Factory location map.
* Route-volume analysis.
* Data explorer with CSV download options.

### Data Quality Note

The dataset contains unusually long shipping lead times based on the recorded order and ship dates. These dates require verification before making conclusions about delivery speed or shipping efficiency.

### How to Run the Dashboard

1. Install the required Python packages.
2. Open a terminal in the project directory.
3. Run the following command:

```bash
python -m streamlit run app.py
```

### Project Status

Developed as part of a data analysis internship project.
