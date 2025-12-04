import csv
from functools import reduce
from datetime import datetime
import os

class SaleRecord:
    """Represents a single sale transaction."""
    
    def __init__(self, row_dict):
        """Initialize sale record from CSV row."""
        self.region = row_dict.get('Region', '')
        self.country = row_dict.get('Country', '')
        self.item_type = row_dict.get('Item Type', '')
        self.sales_channel = row_dict.get('Sales Channel', '')
        self.order_priority = row_dict.get('Order Priority', '')
        self.order_date = row_dict.get('Order Date', '')
        self.order_id = row_dict.get('Order ID', '')
        self.units_sold = int(row_dict.get('Units Sold', 0))
        self.unit_price = float(row_dict.get('Unit Price', 0.0))
        self.sales = float(row_dict.get('Sales', 0.0))
        self.profit = float(row_dict.get('Profit', 0.0))
        self.province = row_dict.get('Province', '')
        self.customer_segment = row_dict.get('Customer Segment', '')
        self.product_category = row_dict.get('Product Category', '')


class SalesAnalyzer:
    """
    Analyzes sales data using functional programming.
    Demonstrates map, filter, reduce, and lambda expressions.
    """
    
    def __init__(self, csv_filepath):
        """Initialize analyzer and load CSV data."""
        self.csv_filepath = csv_filepath
        self.data = []
        self.output_file = "outputs/analysis_results.txt"
        self.load_from_csv()
    
    def load_from_csv(self):
        """
        Load CSV with automatic encoding detection.
        Tries multiple encodings: utf-8, latin-1, iso-8859-1, cp1252.
        """
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(self.csv_filepath, 'r', encoding=encoding) as file:
                    csv_reader = csv.DictReader(file)
                    # Map: transform CSV rows into SaleRecord objects
                    self.data = list(map(lambda row: SaleRecord(row), csv_reader))
                
                print(f"Loaded {len(self.data)} records (encoding: {encoding})")
                return
            except UnicodeDecodeError:
                continue
        
        raise ValueError(f"Could not read {self.csv_filepath}")
    
    def log(self, message):
        """Print to console and save to file."""
        print(message)
        with open(self.output_file, 'a') as f:
            f.write(message + '\n')
    
    def total_sales_by_region(self):
        """
        Calculate total sales per region using filter and reduce.
        Returns: dict of {region: total_sales}
        """
        self.log("\n=== ANALYSIS 1: Total Sales by Region ===")
        
        regions = set(map(lambda sale: sale.region, self.data))
        result = {}
        
        for region in regions:
            # Filter: get sales for this region
            region_sales = list(filter(lambda sale: sale.region == region, self.data))
            # Reduce: sum all sales
            total = reduce(lambda acc, sale: acc + sale.sales, region_sales, 0)
            result[region] = total
        
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    
    def top_products_by_sales(self, n=10):
        """
        Find top N product categories by sales.
        Returns: list of (product, sales) tuples
        """
        self.log(f"\n=== ANALYSIS 2: Top {n} Products ===")
        
        categories = set(map(lambda sale: sale.product_category, self.data))
        product_sales = []
        
        for category in categories:
            category_sales = list(filter(lambda sale: sale.product_category == category, self.data))
            total = reduce(lambda acc, sale: acc + sale.sales, category_sales, 0)
            product_sales.append((category, total))
        
        return sorted(product_sales, key=lambda x: x[1], reverse=True)[:n]
    
    def average_order_value(self):
        """
        Calculate average sales per order using map and reduce.
        Returns: float
        """
        self.log("\n=== ANALYSIS 3: Average Order Value ===")
        
        all_sales = list(map(lambda sale: sale.sales, self.data))
        total = reduce(lambda acc, sales: acc + sales, all_sales, 0)
        
        return total / len(all_sales) if all_sales else 0
    
    def sales_by_customer_segment(self):
        """
        Compare sales across customer segments.
        Returns: dict of {segment: {sales, count, avg}}
        """
        self.log("\n=== ANALYSIS 4: Sales by Customer Segment ===")
        
        segments = set(map(lambda sale: sale.customer_segment, self.data))
        result = {}
        
        for segment in segments:
            segment_sales = list(filter(lambda sale: sale.customer_segment == segment, self.data))
            total_sales = reduce(lambda acc, sale: acc + sale.sales, segment_sales, 0)
            count = len(segment_sales)
            
            result[segment] = {
                "sales": total_sales,
                "count": count,
                "avg": total_sales / count if count > 0 else 0
            }
        
        return result
    
    def top_provinces_by_profit(self, n=10):
        """
        Find top N provinces by profit.
        Returns: list of (province, profit) tuples
        """
        self.log(f"\n=== ANALYSIS 5: Top {n} Provinces ===")
        
        provinces = set(map(lambda sale: sale.province, self.data))
        province_profits = []
        
        for province in provinces:
            province_sales = list(filter(lambda sale: sale.province == province, self.data))
            total_profit = reduce(lambda acc, sale: acc + sale.profit, province_sales, 0)
            province_profits.append((province, total_profit))
        
        return sorted(province_profits, key=lambda x: x[1], reverse=True)[:n]
    
    def monthly_sales_trend(self):
        """
        Calculate sales per month with date parsing.
        Returns: dict of {month: total_sales}
        """
        self.log("\n=== ANALYSIS 6: Monthly Sales Trend ===")
        
        months = set(map(lambda sale: self._parse_month(sale.order_date), self.data))
        result = {}
        
        for month in sorted(months):
            month_sales = list(filter(lambda sale: self._parse_month(sale.order_date) == month, self.data))
            total = reduce(lambda acc, sale: acc + sale.sales, month_sales, 0)
            result[month] = total
        
        return result
    
    def _parse_month(self, date_str):
        """Helper to extract YYYY-MM from date string."""
        try:
            date_obj = datetime.strptime(date_str, '%m/%d/%Y')
            return date_obj.strftime('%Y-%m')
        except:
            try:
                parts = date_str.split('/')
                return f"{parts[2]}-{parts[0].zfill(2)}"
            except:
                return "Unknown"
    
    def run_all_analyses(self):
        """Execute all analyses and save results."""
        # Create output directory
        os.makedirs('outputs', exist_ok=True)
        
        # Clear previous output
        with open(self.output_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("SALES DATA ANALYSIS REPORT\n")
            f.write(f"Total Records: {len(self.data):,}\n")
            f.write("="*70 + "\n")
        
        self.log("="*70)
        self.log(f"ANALYZING {len(self.data):,} SALES RECORDS")
        self.log("="*70)
        
        # Analysis 1: Sales by Region
        region_sales = self.total_sales_by_region()
        for region, sales in region_sales.items():
            self.log(f"{region}: ${sales:,.2f}")
        
        # Analysis 2: Top Products
        top_products = self.top_products_by_sales(10)
        for rank, (product, sales) in enumerate(top_products, 1):
            self.log(f"#{rank}: {product} - ${sales:,.2f}")
        
        # Analysis 3: Average Order Value
        avg_order = self.average_order_value()
        self.log(f"Average Order Value: ${avg_order:,.2f}")
        
        # Analysis 4: Customer Segments
        segment_data = self.sales_by_customer_segment()
        for segment, metrics in sorted(segment_data.items()):
            self.log(f"{segment}:")
            self.log(f"  Total Sales: ${metrics['sales']:,.2f}")
            self.log(f"  Order Count: {metrics['count']}")
            self.log(f"  Average: ${metrics['avg']:,.2f}")
        
        # Analysis 5: Top Provinces
        top_provinces = self.top_provinces_by_profit(10)
        for rank, (province, profit) in enumerate(top_provinces, 1):
            self.log(f"#{rank}: {province} - ${profit:,.2f}")
        
        # Analysis 6: Monthly Trend (last 12 months)
        monthly_trend = self.monthly_sales_trend()
        for month, sales in sorted(monthly_trend.items())[-12:]:
            self.log(f"{month}: ${sales:,.2f}")
        
        self.log("\n" + "="*70)
        self.log("Analysis complete!")
        self.log("="*70)
        
        print(f"\n✓ Output saved to: {self.output_file}")


if __name__ == "__main__":
    analyzer = SalesAnalyzer("sales_data.csv")
    analyzer.run_all_analyses()