-- Create a staging table for transaction data
CREATE TABLE staging_transactions (
    TransactionID INT PRIMARY KEY,
    CustomerID VARCHAR(10),
    Restaurant VARCHAR(20),
    Location VARCHAR(20),
    Date DATE,                              -- Changed from TransactionDate
    Time TIME,                              -- Changed from TransactionTime
    OrderType VARCHAR(15),
    PaymentMethod VARCHAR(20),
    ItemsOrdered TEXT,
    Subtotal DECIMAL(10,2),
    Discount DECIMAL(10,2),
    Tax DECIMAL(10,2),
    Tip DECIMAL(10,2),
    DeliveryFee DECIMAL(10,2),
    Total DECIMAL(10,2),
    ProcessingTimeMin DECIMAL(10,2),        -- Changed from INT to DECIMAL
    EmployeeID VARCHAR(10),
    Weather VARCHAR(15),
    PromotionCode VARCHAR(15),
    SatisfactionRating DECIMAL(5,2),        -- Changed from INT to DECIMAL
    TransactionType VARCHAR(10),
    RefundReason VARCHAR(50),               -- Added column
    OriginalTransactionID VARCHAR(10),      -- Added column
    IsDuplicate BOOLEAN,                    -- Added column
    IsRefund BOOLEAN,                       -- Added column
    DateTime TIMESTAMP,                     -- Added column
    Year INT,
    Month INT,
    Day INT,                                -- Added column
    DayOfWeek VARCHAR(10),
    Hour INT
);

-- Create a derived KPI table for reporting
CREATE TABLE restaurant_kpis (
    ReportingDate DATE,
    Quarter VARCHAR(6),
    Restaurant VARCHAR(20),
    Location VARCHAR(20),
    TotalTransactions INT,
    TotalRevenue DECIMAL(12,2),
    AverageOrderValue DECIMAL(8,2),
    CustomerRetentionRate DECIMAL(5,2),
    OrderGrowthRate DECIMAL(5,2),
    SatisfactionScore DECIMAL(3,2),
    ProcessingEfficiency DECIMAL(5,2)
);