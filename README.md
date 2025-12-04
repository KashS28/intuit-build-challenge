# Intuit — Assignments

Complete Python implementations demonstrating advanced threading patterns and functional programming for data analysis. This repository contains two comprehensive assignments with full test coverage and detailed documentation.

---
## Quick Reference

### Run All Tests
```bash
# Assignment 1
cd Assignment1_ProducerConsumer && python3 -m unittest test_producer_consumer.py -v

# Assignment 2
cd Assignment2_DataAnalysis && python3 -m unittest test_sales_analyzer.py -v
```

### Run Programs
```bash
# Assignment 1
cd Assignment1_ProducerConsumer && python3 producer_consumer.py

# Assignment 2
cd Assignment2_DataAnalysis && python3 sales_analyzer.py
```

### View Outputs
```bash
# Assignment 1 output
cat Assignment1_ProducerConsumer/outputs/producer_consumer_output.txt

# Assignment 2 output
cat Assignment2_DataAnalysis/outputs/analysis_results.txt
```

---

---

## 📁 Repository Structure
```
intuit-build-challenge/
├── Assignment1_ProducerConsumer/
│   ├── producer_consumer.py
│   ├── test_producer_consumer.py
│   └── outputs/
│       └── producer_consumer_output.txt
│
├── Assignment2_DataAnalysis/
│   ├── sales_analyzer.py
│   ├── test_sales_analyzer.py
│   ├── download_dataset.py
│   ├── sales_data.csv
│   └── outputs/
│       └── analysis_results.txt
│
├── README.md
└── .gitignore
```

---

## Assignment 1: Producer-Consumer Pattern Implementation

### Overview

**Purpose:** Demonstrates thread synchronization, concurrent programming, and the producer-consumer pattern using Python's thread-safe queue.

**Key Files:**
- `producer_consumer.py` — Core implementation with Producer and Consumer classes
- `test_producer_consumer.py` — Comprehensive test suite validating thread safety and synchronization
- `outputs/producer_consumer_output.txt` — Program execution log showing thread coordination

### Architecture

#### **ProducerConsumer Class**

Main orchestrator managing the producer-consumer workflow with thread synchronization.

**Key Attributes:**
```python
self.source              # Input data list
self.destination        # Output data list (populated by consumer)
self.shared_queue       # Thread-safe queue (Queue.Queue with maxsize)
self.producer_thread    # Producer thread instance
self.consumer_thread    # Consumer thread instance
```

#### **Producer Method**

**Purpose:** Reads items from source and places them into shared queue.

**Key Methods:**

| Method | Purpose | Implementation Details |
|--------|---------|----------------------|
| `producer()` | Main producer logic | Iterates through source, puts items in queue (blocks if full), simulates processing with delays |
| `start()` | Orchestrate workflow | Creates threads, starts producer/consumer, waits for completion |

**Thread Synchronization Features:**
- Uses `queue.Queue.put()` — Blocks automatically when queue is full (wait mechanism)
- Handles queue blocking gracefully without explicit lock management
- Updates destination atomically through thread-safe queue operations

**Implementation:**
```python
for item in self.source:
    self.log(f"Producer: Adding {item} to queue")
    self.shared_queue.put(item)  # Blocks if queue is full
    time.sleep(0.5)  # Simulate work
```

#### **Consumer Method**

**Purpose:** Takes items from shared queue and stores them in destination container.

**Key Methods:**

| Method | Purpose | Implementation Details |
|--------|---------|----------------------|
| `consumer()` | Main consumer logic | Gets items from queue (blocks if empty), appends to destination, marks task done |
| `log()` | Output management | Writes to console and output file for audit trail |

**Thread Synchronization Features:**
- Uses `queue.Queue.get()` — Blocks automatically when queue is empty (wait mechanism)
- Calls `queue.task_done()` to signal item completion
- Waits for all queue items to finish before thread completes

**Implementation:**
```python
for _ in range(len(self.source)):
    item = self.shared_queue.get()  # Blocks if queue is empty
    self.destination.append(item)
    self.shared_queue.task_done()   # Mark item as processed
    time.sleep(1)  # Simulate slower consumer
```

### Configuration

**Default Parameters:**
```python
source_data = [1, 2, 3, 4, 5, 6, 7, 8]  # 8 items to process
queue_capacity = 3                        # Queue max size (demonstrates blocking)
producer_speed = 0.5 seconds             # Producer delay per item
consumer_speed = 1.0 seconds             # Consumer delay per item (slower = backpressure)
```

### Workflow Sequence

1. Initialize with source data and queue capacity
2. Create producer and consumer threads
3. Producer iterates source → puts items in queue (blocks if full)
4. Consumer gets items from queue (blocks if empty) → appends to destination
5. Both threads coordinate through shared queue
6. Wait for all threads to complete (`join()`)
7. Validate: source == destination

### Test Suite

All tests validate thread synchronization, concurrent programming, and blocking queue behavior.

| Test # | Test Name | Purpose | What It Validates |
|--------|-----------|---------|-------------------|
| **1** | `test_basic_functionality` | Core transfer logic | - All items transfer correctly<br>- Source equals destination<br>- Item order preserved |
| **2** | `test_empty_source` | Edge case handling | - Empty source handled gracefully<br>- No items processed<br>- No errors on empty queue |
| **3** | `test_single_item` | Minimal dataset | - Single item processes correctly<br>- Queue capacity respected<br>- Thread completion works |
| **4** | `test_large_dataset` | Scalability test | - 50 items process correctly<br>- Large queue operations work<br>- No data loss with scaling |
| **5** | `test_thread_safety` | Concurrent stress test | - 100 items maintain integrity<br>- No race conditions<br>- Destination items match source<br>- All items accounted for |

### Thread Synchronization Mechanisms

**1. BlockingQueue (Queue.Queue)**
```python
self.shared_queue = queue.Queue(maxsize=3)
self.shared_queue.put(item)        # Blocks if queue is full
item = self.shared_queue.get()     # Blocks if queue is empty
self.shared_queue.task_done()      # Signal item completion
```

**Benefits:**
- Automatic wait/notify mechanism
- No manual lock management needed
- Handles backpressure naturally (producer waits if consumer lags)
- Prevents data loss through queue blocking

**2. Thread Joining**
```python
self.producer_thread.join()        # Wait for producer to finish
self.consumer_thread.join()        # Wait for consumer to finish
self.shared_queue.join()           # Wait for all queued items processed
```

**3. Shared Data Structure (destination list)**
```python
# Consumer appends safely (single writer pattern)
self.destination.append(item)
```

### How to Run

**Prerequisites**
- Python 3.8 or higher
- No external packages required (uses standard library: `threading`, `queue`)

**Compile/Setup**
```bash
cd Assignment1_ProducerConsumer
```

**Run Main Program**
```bash
python3 producer_consumer.py
```

**Run Tests**
```bash
python3 -m unittest test_producer_consumer.py -v
```

**Expected Output:**
```
test_basic_functionality (test_producer_consumer.TestProducerConsumer) ... ok
test_empty_source (test_producer_consumer.TestProducerConsumer) ... ok
test_single_item (test_producer_consumer.TestProducerConsumer) ... ok
test_large_dataset (test_producer_consumer.TestProducerConsumer) ... ok
test_thread_safety (test_producer_consumer.TestProducerConsumer) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.523s

OK
```

**Program Output Example**
```
=== PRODUCER-CONSUMER PATTERN OUTPUT ===

Source data: [1, 2, 3, 4, 5, 6, 7, 8]
Queue capacity: 3

Producer: Starting to produce items
Producer: Adding 1 to queue
Producer: Successfully added 1 (Queue size: 1)
Consumer: Starting to consume items
Producer: Adding 2 to queue
Consumer: Trying to get item from queue
Consumer: Got 1 from queue
Producer: Successfully added 2 (Queue size: 1)
Producer: Adding 3 to queue
Producer: Successfully added 3 (Queue size: 2)
Producer: Adding 4 to queue
Producer: Successfully added 4 (Queue size: 3)
Producer: Adding 5 to queue
(Producer blocks - queue is full, waiting for consumer)
Consumer: Stored 1 in destination (Total: 1)
Consumer: Trying to get item from queue
Consumer: Got 2 from queue
Producer: Successfully added 5 (Queue size: 3)
Producer: Adding 6 to queue
(Producer blocks again)
...continuing until all items processed...
Producer: Finished producing all items
Consumer: Finished consuming all items

=== COMPLETE ===
Final destination: [1, 2, 3, 4, 5, 6, 7, 8]
Items processed: 8
Success: True
```

### Why This Design?

- **BlockingQueue**: Handles synchronization automatically — producer waits if queue full, consumer waits if empty
- **Separate Threads**: Demonstrates true concurrent execution and coordination
- **Backpressure Handling**: Slower consumer naturally throttles producer
- **Simple yet Realistic**: Shows real-world pattern used in data pipelines, message brokers, thread pools

### Testing Objectives Met

| Objective | Implementation | Test Coverage |
|-----------|---------------|---------------|
| **Thread Synchronization** | BlockingQueue operations | Tests 1, 2, 3 |
| **Concurrent Programming** | Producer/Consumer threads | Tests 4, 5 |
| **Blocking Queues** | Queue.Queue with maxsize | All tests |
| **Wait/Notify Mechanism** | Implicit in Queue operations | All tests |
| **Data Integrity** | Append-only destination list | Tests 1, 4, 5 |
| **Edge Cases** | Empty source, single item, large datasets | Tests 2, 3, 4, 5 |

---

## Assignment 2: Sales Data Analysis with Functional Programming

### Overview

**Purpose:** Demonstrates functional programming techniques (map, filter, reduce) applied to real-world sales data analysis using CSV dataset.

**Key Files:**
- `sales_analyzer.py` — Core analysis implementation using functional paradigms
- `test_sales_analyzer.py` — Unit tests validating all analysis methods
- `sales_data.csv` — Sales dataset (8,399 records from multiple regions and time periods)
- `outputs/analysis_results.txt` — Console output showing all analysis results

### Architecture


**Two-Class Design:**

1. **SaleRecord** - Data model for individual sale transactions
   - Stores: region, product_category, sales, profit, customer_segment, province, order_date
   - Purpose: Type-safe representation of CSV rows

2. **SalesAnalyzer** - Analysis engine using functional programming
   - Loads: CSV with automatic encoding detection
   - Analyzes: 6 different aggregations using map/filter/reduce
   - Outputs: Results to console and file

**Processing Pipeline:**
```
CSV File → map(create SaleRecord) → filter(by criteria) → reduce(aggregate) → Results
```


### Dataset Selection and Assumptions

#### **Dataset Choice: Superstore Sales Dataset**

**Source:** https://raw.githubusercontent.com/curran/data/gh-pages/superstoreSales/superstoreSales.csv

**Selection Rationale:**

1. **Real-world data:** Actual retail transactions with realistic financial metrics
2. **Optimal size:** 8,399 records - large enough for meaningful analysis, manageable for processing
3. **Rich dimensions:** 8 regions, 13+ provinces, 3 product categories, 4 customer segments
4. **Temporal depth:** 4 years of data (2010-2014) for trend analysis
5. **Functional programming fit:** Natural hierarchies ideal for map/filter/reduce demonstrations
6. **Industry standard:** Widely recognized dataset showing familiarity with business analytics

**Why not alternatives?** Kaggle datasets require accounts; synthetic data lacks authenticity; smaller datasets don't demonstrate scalability.

#### **Key Assumptions**

**Data Integrity:**
- All transactions are completed sales (no cancellations/returns)
- Financial metrics (Sales, Profit, Cost) are pre-calculated and accurate
- No duplicate Order IDs

**Formatting:**
- Dates in M/D/YYYY format (e.g., 10/13/2010)
- All monetary values in USD
- CSV encoding handled automatically (utf-8, latin-1, iso-8859-1, cp1252)

**Business Context:**
- Customer segments: Consumer, Corporate, Home Office, Small Business
- Regions represent North American geographic areas
- Product categories: Technology, Furniture, Office Supplies

**Technical:**
- File size manageable for in-memory processing
- Single-threaded analysis (no concurrent access concerns)
- Type conversions: string → int/float as specified in schema

---

### Analysis Methods

#### **1. Total Sales by Region**

**Method:** `total_sales_by_region()`

**Functional Approach:**
```python
# Group records by region using reduce()
# Sum sales for each region
# Sort by sales descending
```

**Sample Output:**
```
=== ANALYSIS 1: Total Sales by Region ===
West: $3,597,549.28
Ontario: $3,063,212.48
Prarie: $2,837,304.60
Atlantic: $2,014,248.20
Quebec: $1,510,195.08
Yukon: $975,867.37
Northwest Territories: $800,847.33
Nunavut: $116,376.48
```

**Use Case:** Regional performance analysis, quota allocation

#### **2. Top Products by Sales**

**Method:** `top_products_by_sales(limit=10)`

**Functional Approach:**
```python
# Group by product category using reduce()
# Calculate total sales per product
# Sort descending and take top N
```

**Sample Output:**
```
=== ANALYSIS 2: Top 10 Products ===
#1: Technology - $5,984,248.18
#2: Furniture - $5,178,590.54
#3: Office Supplies - $3,752,762.10
```

**Use Case:** Product performance ranking, inventory focus

#### **3. Average Order Value**

**Method:** `average_order_value()`

**Functional Approach:**
```python
# Map: extract sales amounts
# Reduce: sum all sales
# Divide by count
```

**Sample Output:**
```
=== ANALYSIS 3: Average Order Value ===
Average Order Value: $1,775.88
```

**Use Case:** Sales metrics, performance indicators

#### **4. Sales by Customer Segment**

**Method:** `sales_by_customer_segment()`

**Functional Approach:**
```python
# Group by segment using reduce()
# Calculate: total sales, order count, average value
# Format with metrics
```

**Sample Output:**
```
=== ANALYSIS 4: Sales by Customer Segment ===
Consumer:
  Total Sales: $3,063,611.08
  Order Count: 1649
  Average: $1,857.86
Corporate:
  Total Sales: $5,498,904.88
  Order Count: 3076
  Average: $1,787.68
Home Office:
  Total Sales: $3,564,763.87
  Order Count: 2032
  Average: $1,754.31
Small Business:
  Total Sales: $2,788,320.99
  Order Count: 1642
  Average: $1,698.12
```

**Use Case:** Customer analytics, segment strategy

#### **5. Top Provinces by Profit**

**Method:** `top_provinces_by_profit(limit=10)`

**Functional Approach:**
```python
# Filter: non-empty provinces
# Group by province using reduce()
# Calculate profit per province
# Sort descending, take top N
```

**Sample Output:**
```
=== ANALYSIS 5: Top 10 Provinces ===
#1: Ontario - $346,868.54
#2: Saskachewan - $184,732.96
#3: Alberta - $151,946.48
#4: British Columbia - $145,062.13
#5: Quebec - $140,426.65
#6: Manitoba - $136,427.16
#7: New Brunswick - $115,351.94
#8: Northwest Territories - $100,653.08
#9: Nova Scotia - $85,361.87
#10: Yukon - $73,849.21
```

**Use Case:** Geographic profitability analysis, regional focus

#### **6. Monthly Sales Trend**

**Method:** `monthly_sales_trend()`

**Functional Approach:**
```python
# Map: extract dates and sales
# Group by month (YYYY-MM) using reduce()
# Sum sales per month
# Sort chronologically
```

**Sample Output:**
```
=== ANALYSIS 6: Monthly Sales Trend ===
2012-01: $340,626.51
2012-02: $276,132.50
2012-03: $348,208.33
2012-04: $268,024.97
2012-05: $384,588.06
2012-06: $276,580.94
2012-07: $242,809.70
2012-08: $302,745.12
2012-09: $318,271.57
2012-10: $351,246.73
2012-11: $256,020.10
2012-12: $354,709.34
```

**Use Case:** Seasonality analysis, trend forecasting

### Functional Programming Techniques

#### **1. Map (Transform)**
```python
# Transform CSV rows into SaleRecord objects
self.data = list(map(lambda row: SaleRecord(row), csv_reader))

# Extract specific fields
sales_amounts = list(map(lambda r: r.sales, self.data))
```

**Purpose:** Convert raw data into usable objects or extract specific fields

#### **2. Filter (Select)**
```python
# Filter records by condition
profitable = list(filter(lambda r: r.profit > 0, self.data))

# Filter non-empty values
provinces = list(filter(lambda p: p != '', province_list))
```

**Purpose:** Keep only records meeting specific criteria

#### **3. Reduce (Aggregate)**
```python
# Group by region and sum sales
from functools import reduce

by_region = reduce(
    lambda acc, r: {**acc, r.region: acc.get(r.region, 0) + r.sales},
    self.data,
    {}
)

# Calculate total
total = reduce(lambda acc, r: acc + r.sales, self.data, 0)
```

**Purpose:** Aggregate data into summary statistics

#### **4. Lambda Expressions**
```python
# Short anonymous functions for sorting, filtering, mapping
sorted_data = sorted(records, key=lambda r: r.sales, reverse=True)
```

### Test Suite

All tests validate data loading, calculations, and functional programming patterns.

| Test # | Test Name | Purpose | What It Validates |
|--------|-----------|---------|-------------------|
| **1** | `test_record_initialization` | Data model | - CSV row parsing correct<br>- Type conversions accurate<br>- All fields populated |
| **2** | `test_load_from_csv` | CSV loading | - All 8,399 records loaded<br>- Encoding detection works<br>- SaleRecord objects created |
| **3** | `test_total_sales_by_region` | Region aggregation | - All regions included<br>- Sales totals accurate<br>- Dictionary format correct |
| **4** | `test_top_products_by_sales` | Product ranking | - Top products identified<br>- Sorted descending<br>- Limit parameter respected |
| **5** | `test_average_order_value` | Average calculation | - Correct computation<br>- Float precision<br>- Matches manual calculation |
| **6** | `test_sales_by_customer_segment` | Segment analysis | - All segments included<br>- Metrics accurate<br>- Count and avg correct |
| **7** | `test_top_provinces_by_profit` | Province ranking | - Top provinces identified<br>- Profit totals correct<br>- Descending order verified |

### How to Run

**Prerequisites**
- Python 3.8 or higher
- No external packages required (uses standard library: `csv`, `functools`, `datetime`)

**Setup**
```bash
cd Assignment2_DataAnalysis
```

**Run Main Analysis Program**
```bash
python3 sales_analyzer.py
```

**Run Tests**
```bash
python3 -m unittest test_sales_analyzer.py -v
```

**Expected Output:**
```
test_load_from_csv (test_sales_analyzer.TestSalesAnalyzer) ... ok
test_record_initialization (test_sales_analyzer.TestSaleRecord) ... ok
test_sales_by_customer_segment (test_sales_analyzer.TestSalesAnalyzer) ... ok
test_top_products_by_sales (test_sales_analyzer.TestSalesAnalyzer) ... ok
test_total_sales_by_region (test_sales_analyzer.TestSalesAnalyzer) ... ok
test_average_order_value (test_sales_analyzer.TestSalesAnalyzer) ... ok
test_top_provinces_by_profit (test_sales_analyzer.TestSalesAnalyzer) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.245s

OK
```

**Analysis Output**
```
Loaded 8,399 records (encoding: utf-8)

======================================================================
SALES DATA ANALYSIS REPORT
Total Records: 8,399
======================================================================
======================================================================
ANALYZING 8,399 SALES RECORDS
======================================================================

=== ANALYSIS 1: Total Sales by Region ===
West: $3,597,549.28
Ontario: $3,063,212.48
Prarie: $2,837,304.60
Atlantic: $2,014,248.20
Quebec: $1,510,195.08
Yukon: $975,867.37
Northwest Territories: $800,847.33
Nunavut: $116,376.48

=== ANALYSIS 2: Top 10 Products ===
#1: Technology - $5,984,248.18
#2: Furniture - $5,178,590.54
#3: Office Supplies - $3,752,762.10

=== ANALYSIS 3: Average Order Value ===
Average Order Value: $1,775.88

=== ANALYSIS 4: Sales by Customer Segment ===
Consumer:
  Total Sales: $3,063,611.08
  Order Count: 1649
  Average: $1,857.86
Corporate:
  Total Sales: $5,498,904.88
  Order Count: 3076
  Average: $1,787.68
Home Office:
  Total Sales: $3,564,763.87
  Order Count: 2032
  Average: $1,754.31
Small Business:
  Total Sales: $2,788,320.99
  Order Count: 1642
  Average: $1,698.12

=== ANALYSIS 5: Top 10 Provinces ===
#1: Ontario - $346,868.54
#2: Saskachewan - $184,732.96
#3: Alberta - $151,946.48
#4: British Columbia - $145,062.13
#5: Quebec - $140,426.65
#6: Manitoba - $136,427.16
#7: New Brunswick - $115,351.94
#8: Northwest Territories - $100,653.08
#9: Nova Scotia - $85,361.87
#10: Yukon - $73,849.21

=== ANALYSIS 6: Monthly Sales Trend ===
2012-01: $340,626.51
2012-02: $276,132.50
2012-03: $348,208.33
2012-04: $268,024.97
2012-05: $384,588.06
2012-06: $276,580.94
2012-07: $242,809.70
2012-08: $302,745.12
2012-09: $318,271.57
2012-10: $351,246.73
2012-11: $256,020.10
2012-12: $354,709.34

======================================================================
Analysis complete!
======================================================================
```

### Why This Design?

- **Functional Approach**: Uses map/filter/reduce instead of loops — more expressive and concise
- **Lambda Expressions**: Clean, readable code for transformations
- **Reduce for Aggregation**: Powerful for grouping and summing complex operations
- **Data Model (SaleRecord)**: Provides type safety and clear structure
- **Encoding Detection**: Handles various CSV formats gracefully

### Testing Objectives Met

| Objective | Implementation | Test Coverage |
|-----------|---------------|---------------|
| **Functional Programming** | Map, filter, reduce | All tests |
| **Data Loading** | CSV with encoding detection | Test 2 |
| **Type Conversion** | String → numeric/object | Test 1 |
| **Aggregation** | Reduce-based grouping | Tests 3, 6, 7 |
| **Calculations** | Sum, average, count | Tests 3, 5, 6 |
| **Sorting/Ranking** | Lambda for key extraction | Tests 4, 7 |

---

## Deliverables Summary

### Assignment 1: Producer-Consumer Pattern
✅ Complete source code (`producer_consumer.py`)  
✅ Unit tests with 5 comprehensive test cases  
✅ Detailed README (above) with setup and sample output  
✅ Console execution log to `outputs/producer_consumer_output.txt`  

### Assignment 2: Sales Data Analysis
✅ Complete source code (`sales_analyzer.py`)  
✅ Unit tests with 7 comprehensive test cases  
✅ Detailed README (above) with setup and sample output  
✅ Analysis results printed to console and saved to `outputs/analysis_results.txt`  

---
