# Intuit — Assignments

Python implementations of thread synchronization and functional data analysis. Both assignments demonstrate core programming competencies with comprehensive tests and clear documentation.

---

## Quick Start

**Prerequisites:** Python 3.8+

```bash
# Run all tests
cd Assignment1_ProducerConsumer && python3 -m unittest test_producer_consumer.py -v
cd ../Assignment2_DataAnalysis && python3 -m unittest test_sales_analyzer.py -v

# Run programs
cd Assignment1_ProducerConsumer && python3 producer_consumer.py
cd ../Assignment2_DataAnalysis && python3 sales_analyzer.py

# View outputs
cat Assignment1_ProducerConsumer/outputs/producer_consumer_output.txt
cat Assignment2_DataAnalysis/outputs/analysis_results.txt
```

---

## Assignment 1: Producer-Consumer Pattern

**Demonstrates:** Thread synchronization, concurrent programming, blocking queues, wait/notify mechanisms

### Architecture

- **ProducerConsumer class:** Manages producer/consumer coordination
- **Producer method:** Reads from source, puts items in queue (blocks if full)
- **Consumer method:** Gets items from queue (blocks if empty), stores in destination
- **Thread safety:** Uses `Queue.Queue` for automatic synchronization

### Key Implementation

```python
# Producer blocks when queue is full
self.shared_queue.put(item)  # Automatic wait

# Consumer blocks when queue is empty
item = self.shared_queue.get()  # Automatic wait
self.shared_queue.task_done()   # Signal completion
```

### Test Coverage (5 tests)

| Test | Validates |
|------|-----------|
| `test_basic_functionality` | Core transfer, order preservation |
| `test_empty_source` | Edge case handling |
| `test_single_item` | Minimal dataset |
| `test_large_dataset` | 50-item scalability |
| `test_thread_safety` | 100-item stress test, no race conditions |

### Sample Output

```
Source data: [1, 2, 3, 4, 5, 6, 7, 8]
Queue capacity: 3

Producer: Starting to produce items
Consumer: Starting to consume items
Producer: Adding 1 to queue
Consumer: Got 1 from queue
...continues until complete...

=== COMPLETE ===
Final destination: [1, 2, 3, 4, 5, 6, 7, 8]
Items processed: 8
Success: True
```

---

## Assignment 2: Sales Data Analysis

**Demonstrates:** Functional programming (map/filter/reduce), data aggregation, lambda expressions

### Architecture

- **SaleRecord class:** Data model for individual transactions
- **SalesAnalyzer class:** Analysis engine using functional paradigms
- **CSV loading:** Automatic encoding detection (utf-8, latin-1, iso-8859-1, cp1252)
- **6 analyses:** Region sales, top products, average order value, customer segments, top provinces, monthly trends

### Key Techniques

```python
# Map: Transform CSV rows to objects
self.data = list(map(lambda row: SaleRecord(row), csv_reader))

# Filter: Select specific records
profitable = list(filter(lambda r: r.profit > 0, self.data))

# Reduce: Aggregate into summaries
total = reduce(lambda acc, r: acc + r.sales, self.data, 0)
```

### Dataset

- **Source:** Superstore Sales (8,399 records)
- **Includes:** 8 regions, 13+ provinces, 3 product categories, 4 customer segments
- **Time period:** 4 years of transaction data
- **Choice rationale:** Real-world data, optimal size for analysis, rich dimensions for functional programming demonstrations

### Test Coverage (7 tests)

| Test | Validates |
|------|-----------|
| `test_record_initialization` | CSV row parsing, type conversions |
| `test_load_from_csv` | All 8,399 records loaded, encoding detection |
| `test_total_sales_by_region` | Region grouping, sales accuracy |
| `test_top_products_by_sales` | Product ranking, sort order |
| `test_average_order_value` | Calculation accuracy |
| `test_sales_by_customer_segment` | Segment aggregation, metrics |
| `test_top_provinces_by_profit` | Province ranking, profit totals |

### Sample Output

```
=== ANALYSIS 1: Total Sales by Region ===
West: $3,597,549.28
Ontario: $3,063,212.48
...

=== ANALYSIS 4: Sales by Customer Segment ===
Consumer: Total Sales: $3,063,611.08 (1,649 orders, avg: $1,857.86)
Corporate: Total Sales: $5,498,904.88 (3,076 orders, avg: $1,787.68)
...

=== ANALYSIS 6: Monthly Sales Trend ===
2012-01: $340,626.51
2012-02: $276,132.50
...
```

---

## Repository Structure

```
Assignment1_ProducerConsumer/
├── producer_consumer.py
├── test_producer_consumer.py
└── outputs/producer_consumer_output.txt

Assignment2_DataAnalysis/
├── sales_analyzer.py
├── test_sales_analyzer.py
├── sales_data.csv
└── outputs/analysis_results.txt

README.md
```

---

## Test Results

**Assignment 1:** 5/5 tests passing ✅  
**Assignment 2:** 7/7 tests passing ✅

---

