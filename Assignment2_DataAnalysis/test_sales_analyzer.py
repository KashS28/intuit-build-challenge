import unittest
import os
from sales_analyzer import SalesAnalyzer, SaleRecord

class TestSaleRecord(unittest.TestCase):
    """Test SaleRecord initialization."""
    
    def test_record_initialization(self):
        """Test that SaleRecord parses CSV row correctly."""
        test_dict = {
            'Region': 'Europe',
            'Country': 'France',
            'Item Type': 'Cosmetics',
            'Sales Channel': 'Online',
            'Order Priority': 'H',
            'Order Date': '5/22/2017',
            'Order ID': '898523128',
            'Units Sold': '1815',
            'Unit Price': '437.20',
            'Sales': '793518.00',
            'Profit': '315574.05',
            'Province': 'Quebec',
            'Customer Segment': 'Consumer',
            'Product Category': 'Technology'
        }
        
        sale = SaleRecord(test_dict)
        
        self.assertEqual('Europe', sale.region)
        self.assertEqual('Technology', sale.product_category)
        self.assertEqual(1815, sale.units_sold)
        self.assertEqual(793518.00, sale.sales)


class TestSalesAnalyzer(unittest.TestCase):
    """Test suite for SalesAnalyzer."""
    
    def setUp(self):
        """Load data before each test."""
        if not os.path.exists("sales_data.csv"):
            self.skipTest("sales_data.csv not found")
        
        self.analyzer = SalesAnalyzer("sales_data.csv")
    
    def test_load_from_csv(self):
        """Test CSV loading."""
        self.assertGreater(len(self.analyzer.data), 1000)
        self.assertIsInstance(self.analyzer.data[0], SaleRecord)
    
    def test_total_sales_by_region(self):
        """Test region aggregation."""
        result = self.analyzer.total_sales_by_region()
        
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)
        
        for region, sales in result.items():
            self.assertGreater(sales, 0)
    
    def test_top_products_by_sales(self):
        """Test product ranking."""
        result = self.analyzer.top_products_by_sales(10)
        
        self.assertGreater(len(result), 0)
        self.assertLessEqual(len(result), 10)
        
        # Check descending order
        for i in range(len(result) - 1):
            self.assertGreaterEqual(result[i][1], result[i+1][1])
    
    def test_average_order_value(self):
        """Test average calculation."""
        result = self.analyzer.average_order_value()
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
    
    def test_sales_by_customer_segment(self):
        """Test segment analysis."""
        result = self.analyzer.sales_by_customer_segment()
        
        self.assertGreater(len(result), 0)
        
        for segment, metrics in result.items():
            self.assertIn('sales', metrics)
            self.assertIn('count', metrics)
            self.assertIn('avg', metrics)
    
    def test_top_provinces_by_profit(self):
        """Test province ranking."""
        result = self.analyzer.top_provinces_by_profit(10)
        
        self.assertLessEqual(len(result), 10)
        
        # Check descending order
        for i in range(len(result) - 1):
            self.assertGreaterEqual(result[i][1], result[i+1][1])


if __name__ == '__main__':
    unittest.main()