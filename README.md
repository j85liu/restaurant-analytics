# restaurant-analytics

restaurant-analytics/
│
├── data/
│   ├── restaurant_transactions_cleaned.xlsx   # Cleaned transaction data
│   └── restaurant_transactions_cleaned.csv    # CSV version of cleaned data
│
├── output/
│   ├── restaurant_kpis.csv                    # Generated KPI metrics
│   ├── customer_retention.csv                 # Customer retention analysis
│   └── quarterly_forecasts.csv                # Revenue forecasts
│
├── lib/
│   └── postgresql-42.6.0.jar                  # PostgreSQL JDBC driver
│
├── sql/
│   ├── schema.sql                             # Database schema
│   └── queries.sql                            # KPI queries
│
├── spark/
│   ├── data_processing.py                     # PySpark data transformation
│   └── time_series.py                         # Time series analysis
│
├── forecasting/
│   └── prophet_forecast.py                    # Forecasting models
│
├── pipeline/
│   └── etl_pipeline.py                        # ETL pipeline code
│
├── tableau/
│   ├── restaurant_analytics.twbx              # Tableau workbook
│   └── README.md                              # Documentation for Tableau workbooks
│
├── README.md                                  # Project overview
└── requirements.txt                           # Python dependencies

# Restaurant Chain Performance Analytics

## Project Overview
This project demonstrates the analysis of transaction data from multiple restaurant chains to derive business insights, calculate KPIs, and forecast future performance. It showcases my ability to leverage consumer transaction data to produce bi-quarterly estimates and reports similar to my experience analyzing companies like DPZ, WEN, QSR, and PZZA.

## Skills Demonstrated
- **Data Processing**: Using PySpark to process and analyze large datasets
- **KPI Development**: Creating and tracking key performance indicators
- **Forecasting**: Building time-series forecasts for future quarters
- **Data Visualization**: Designing comprehensive Tableau dashboards
- **ETL Pipeline Design**: Creating reproducible data workflows

## Data Pipeline
1. **Data Acquisition**: Simulated transaction data for four restaurant chains
2. **Data Cleaning**: Handled refunds, duplicates, and formatting inconsistencies
3. **Data Transformation**: Used PySpark for large-scale data processing
4. **KPI Calculation**: Generated metrics including:
   - Average Order Value
   - Customer Retention Rate
   - Revenue Growth
   - Operational Efficiency
5. **Forecasting**: Created time-series forecasts for upcoming quarters
6. **Visualization**: Developed Tableau dashboards for stakeholder presentation

## Key Findings
- Restaurant X shows the highest average order value but lowest customer retention
- Location Y consistently outperforms other locations across all restaurant chains
- Weather conditions significantly impact delivery orders
- Customer retention shows strong seasonal patterns
- [Other insights from your analysis]

## Tools Used
- **Apache Spark**: For large-scale data processing
- **PostgreSQL**: For data storage and retrieval
- **Tableau**: For visualization and dashboard creation
- **Python**: For data pipeline orchestration

## Future Enhancements
- Integrate more advanced forecasting methods (ARIMA, Prophet)
- Add real-time data streaming capabilities
- Develop ML models to predict customer churn

## How This Relates to My Professional Experience
This project demonstrates similar techniques to those I used when analyzing consumer transaction data for publicly traded companies. The approach of synthesizing large datasets, calculating KPIs, and presenting findings through visualizations mirrors my professional work in analyzing restaurant chains and technology companies.