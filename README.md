# Online Retail Customer Segmentation & Analytics

An end-to-end Machine Learning project that analyzes online retail customer purchasing behavior, segments customers using RFM analysis and K-Means clustering, detects unusual customer behavior, and presents business insights through an interactive Streamlit dashboard.

## Project Overview

Understanding customer behavior is important for improving customer retention, increasing revenue, and building effective marketing strategies.

This project uses the Online Retail dataset to analyze customer transactions and identify meaningful customer groups based on their purchasing behavior.

The project combines:
- Exploratory Data Analysis (EDA)
- Data Cleaning and Preprocessing
- RFM Analysis
- Feature Scaling
- K-Means Clustering
- PCA Visualization
- Anomaly Detection using Isolation Forest
- Model Evaluation
- Interactive Streamlit Dashboard

##  Project Objectives

- Understand customer purchasing patterns.
- Identify high-value and low-value customers.
- Segment customers based on Recency, Frequency, and Monetary value.
- Discover unusual purchasing behavior.
- Generate actionable business recommendations.
- Build an interactive analytics dashboard.

##  Dataset

**Dataset:** Online Retail Dataset  
**Source:** UCI Machine Learning Repository

The dataset contains transactions from a UK-based online retail business.

Dataset link: https://archive.ics.uci.edu/dataset/352/online+retail

Important columns:

| Column | Description |
|---|---|
| InvoiceNo | Transaction invoice number |
| StockCode | Product code |
| Description | Product description |
| Quantity | Purchased quantity |
| InvoiceDate | Transaction date |
| UnitPrice | Product price |
| CustomerID | Customer identifier |
| Country | Customer country |

##  Machine Learning Workflow

### 1. Exploratory Data Analysis
- Understand dataset structure.
- Analyze missing values and duplicates.
- Study customer and transaction patterns.
- Explore sales and product trends.

### 2. Data Preprocessing
- Handle missing CustomerID values.
- Remove duplicate records.
- Remove cancelled transactions.
- Handle invalid quantities and prices.
- Create TotalAmount using Quantity × UnitPrice.

### 3. RFM Analysis

RFM stands for:

- **Recency:** How recently a customer purchased.
- **Frequency:** How often a customer purchased.
- **Monetary:** How much a customer spent.

RFM features help understand customer purchasing behavior.

### 4. Feature Scaling

Apply log transformation and StandardScaler to prepare RFM features for clustering.

### 5. K-Means Clustering

Use K-Means to group customers based on their purchasing patterns.

The optimal number of clusters should be selected using appropriate evaluation techniques such as the Elbow Method and Silhouette Score.

### 6. PCA Visualization

Use Principal Component Analysis (PCA) to reduce feature dimensions and visualize customer clusters.

### 7. Anomaly Detection

Use Isolation Forest to identify unusual customer purchasing patterns.

### 8. Model Evaluation

Evaluate clustering performance using:

- Elbow Method
- Silhouette Score
- Davies-Bouldin Score

##  Customer Business Segments

The dashboard uses RFM scores to assign business-oriented customer labels.

| Segment | Business Interpretation |
|---|---|
| Champions | High-value and highly engaged customers |
| Loyal Buyers | Regular purchasing customers |
| Growing Buyers | Customers with growth potential |
| Needs Attention | Customers who may need re-engagement |
| Inactive | Customers with low recent engagement |

**Note:** These RFM business segments are rule-based labels. They are separate from the K-Means cluster labels.

##  Business Insights & Recommendations

| Customer Group | Recommended Strategy |
|---|---|
| Champions | VIP rewards and exclusive offers |
| Loyal Buyers | Loyalty points and membership programs |
| Growing Buyers | Cross-selling and product recommendations |
| Needs Attention | Personalized discounts and reminders |
| Inactive | Win-back campaigns and reactivation offers |

### Expected Business Benefits

- Improve customer retention.
- Identify valuable customer groups.
- Support targeted marketing campaigns.
- Discover unusual purchasing behavior.
- Improve customer engagement.
- Support data-driven business decisions.

These are potential benefits; their actual impact should be validated using campaign results.

##  Interactive Dashboard

The Streamlit dashboard provides:

- Customer overview and KPI metrics.
- Customer segment distribution.
- Revenue analysis.
- RFM heatmap.
- Customer purchasing behavior.
- Business insights and recommendations.
- Customer-level data exploration.
- Anomaly detection results.
- CSV report downloads.

## Project Structure

```text
Online_Retail_ML/
│
├── data/
│   ├── raw/
│   │   └── Online_Retail.xlsx
│   │
│   └── processed/
│       ├── final_customer_segments.csv
│       └── customer_anomalies.csv
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Data_Preprocessing.ipynb
│   ├── 03_RFM_Analysis.ipynb
│   ├── 04_Feature_Scaling.ipynb
│   ├── 05_KMeans_Clustering.ipynb
│   ├── 06_PCA_Visualization.ipynb
│   ├── 07_Anomaly_Detection.ipynb
│   └── 08_Project_Evaluation.ipynb
│
├── models/
├── visualizations/
├── app.py
├── requirements.txt
└── README.md
```

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Plotly
- Streamlit
- Jupyter Notebook


