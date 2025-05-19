from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import os

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Restaurant Analytics") \
    .getOrCreate()

# Get path to the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
csv_path = os.path.join(project_root, "data", "restaurant_transactions_cleaned.csv")
print(f"Reading data from: {csv_path}")

# Read the CSV file
df = spark.read.csv(
    csv_path,
    header=True,
    inferSchema=True
)

print("Successfully read data!")

# Convert string columns to proper types if needed
df = df.withColumn("Date", to_date(col("Date"))) \
       .withColumn("IsRefund", col("IsRefund").cast("boolean"))

# Show the DataFrame schema
print("DataFrame Schema:")
df.printSchema()

# Show a sample of the data
print("\nSample Data:")
df.show(5, truncate=False)

# Register the DataFrame as a temporary view for SQL queries
df.createOrReplaceTempView("transactions")

# Enhanced KPI query using the new columns
kpi_query = """
SELECT 
    Restaurant,
    Location,
    Year,
    CONCAT('Q', CEIL(Month/3)) as Quarter,
    COUNT(*) as TotalTransactions,
    SUM(CASE WHEN IsRefund = false THEN Total ELSE 0 END) as GrossRevenue,
    SUM(CASE WHEN IsRefund = true THEN Total ELSE 0 END) as RefundAmount,
    SUM(Total) as NetRevenue,
    AVG(CASE WHEN IsRefund = false THEN Total ELSE NULL END) as AverageOrderValue,
    COUNT(DISTINCT CustomerID) as UniqueCustomers,
    AVG(ProcessingTimeMin) as AvgProcessingTime,
    AVG(SatisfactionRating) as AvgSatisfaction,
    COUNT(CASE WHEN IsDuplicate = true THEN 1 ELSE NULL END) as DuplicateTransactions
FROM transactions
WHERE IsRefund = false
GROUP BY Restaurant, Location, Year, CONCAT('Q', CEIL(Month/3))
ORDER BY Year, Quarter, Restaurant, Location
"""

# Execute KPI query
restaurant_kpis = spark.sql(kpi_query)
print("\nCalculated KPIs:")
restaurant_kpis.show(20, truncate=False)

# Calculate customer retention
print("\nCalculating Customer Retention Metrics...")
customer_query = """
WITH first_visits AS (
    SELECT 
        CustomerID,
        MIN(CONCAT(Year, '-', Month)) as first_month
    FROM transactions
    WHERE IsRefund = false
    GROUP BY CustomerID
),
monthly_activity AS (
    SELECT 
        CONCAT(Year, '-', Month) as month,
        CustomerID
    FROM transactions
    WHERE IsRefund = false
    GROUP BY CONCAT(Year, '-', Month), CustomerID
),
retention_matrix AS (
    SELECT
        SUBSTRING(f.first_month, 1, 4) as cohort_year,
        SUBSTRING(f.first_month, 6, 2) as cohort_month,
        COUNT(DISTINCT m.CustomerID) as active_customers,
        COUNT(DISTINCT f.CustomerID) as cohort_size,
        (COUNT(DISTINCT m.CustomerID) * 100.0 / COUNT(DISTINCT f.CustomerID)) as retention_rate
    FROM first_visits f
    JOIN monthly_activity m ON f.CustomerID = m.CustomerID
    GROUP BY SUBSTRING(f.first_month, 1, 4), SUBSTRING(f.first_month, 6, 2)
)
SELECT * FROM retention_matrix
ORDER BY cohort_year, cohort_month
"""

customer_retention = spark.sql(customer_query)
print("\nCustomer Retention by Cohort:")
customer_retention.show()

# Calculate quarterly forecasts
forecast_query = """
WITH quarterly_data AS (
    SELECT 
        Restaurant,
        Year,
        CEIL(Month/3) as Quarter,
        SUM(Total) as QuarterlyRevenue
    FROM transactions
    WHERE IsRefund = false
    GROUP BY Restaurant, Year, CEIL(Month/3)
),
restaurant_quarters AS (
    SELECT 
        Restaurant,
        CONCAT(Year, '-Q', Quarter) as YearQuarter,
        QuarterlyRevenue,
        LAG(QuarterlyRevenue, 1) OVER (PARTITION BY Restaurant ORDER BY Year, Quarter) as PrevQuarter,
        LAG(QuarterlyRevenue, 4) OVER (PARTITION BY Restaurant ORDER BY Year, Quarter) as PrevYear
    FROM quarterly_data
)
SELECT
    Restaurant,
    YearQuarter,
    QuarterlyRevenue,
    PrevQuarter,
    PrevYear,
    -- Simple forecast methods
    CASE 
        WHEN PrevQuarter IS NOT NULL THEN (QuarterlyRevenue / PrevQuarter - 1) * 100 
        ELSE NULL 
    END as QoQ_Growth,
    CASE 
        WHEN PrevYear IS NOT NULL THEN (QuarterlyRevenue / PrevYear - 1) * 100 
        ELSE NULL 
    END as YoY_Growth,
    -- Basic next quarter forecast (average of QoQ and seasonal pattern)
    CASE 
        WHEN PrevQuarter IS NOT NULL THEN 
            QuarterlyRevenue * (1 + ((QuarterlyRevenue / PrevQuarter - 1) * 0.7))
        ELSE QuarterlyRevenue * 1.05 -- Default 5% growth if no history
    END as NextQuarterForecast
FROM restaurant_quarters
ORDER BY Restaurant, YearQuarter
"""

quarterly_forecast = spark.sql(forecast_query)
print("\nQuarterly Revenue Forecast:")
quarterly_forecast.show()

# Create output directory if it doesn't exist
output_dir = os.path.join(project_root, "output")
os.makedirs(output_dir, exist_ok=True)

# Save results to CSV files
print("\nSaving results to CSV files...")

# Save KPI results
kpi_path = os.path.join(output_dir, "restaurant_kpis.csv")
restaurant_kpis.coalesce(1).write.mode("overwrite").option("header", "true").csv(kpi_path)
print(f"KPIs saved to: {output_dir}/restaurant_kpis.csv")

# Save customer retention data
retention_path = os.path.join(output_dir, "customer_retention.csv")
customer_retention.coalesce(1).write.mode("overwrite").option("header", "true").csv(retention_path)
print(f"Customer retention saved to: {output_dir}/customer_retention.csv")

# Save forecast data
forecast_path = os.path.join(output_dir, "quarterly_forecasts.csv")
quarterly_forecast.coalesce(1).write.mode("overwrite").option("header", "true").csv(forecast_path)
print(f"Forecasts saved to: {output_dir}/quarterly_forecasts.csv")

print("\nData processing complete. All results saved to CSV files.")

# Stop Spark session
spark.stop()