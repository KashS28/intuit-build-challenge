import unittest
import threading
import time
from producer_consumer import ProducerConsumer

class TestProducerConsumer(unittest.TestCase):
    """Test suite for ProducerConsumer pattern."""
    
    def test_basic_functionality(self):
        """Test that all items transfer correctly."""
        source = [1, 2, 3, 4, 5]
        pc = ProducerConsumer(source, queue_capacity=2)
        pc.start()
        
        self.assertEqual(source, pc.destination)
        self.assertEqual(len(source), len(pc.destination))
    
    def test_empty_source(self):
        """Test with empty source."""
        source = []
        pc = ProducerConsumer(source, queue_capacity=2)
        pc.start()
        
        self.assertEqual([], pc.destination)
    
    def test_single_item(self):
        """Test with single item."""
        source = [42]
        pc = ProducerConsumer(source, queue_capacity=1)
        pc.start()
        
        self.assertEqual([42], pc.destination)
    
    def test_large_dataset(self):
        """Test with 50 items."""
        source = list(range(1, 51))
        pc = ProducerConsumer(source, queue_capacity=5)
        pc.start()
        
        self.assertEqual(source, pc.destination)
        self.assertEqual(50, len(pc.destination))
    
    def test_thread_safety(self):
        """Test with 100 items for thread safety."""
        source = list(range(1, 101))
        pc = ProducerConsumer(source, queue_capacity=10)
        pc.start()
        
        self.assertEqual(sorted(source), sorted(pc.destination))
        self.assertEqual(len(source), len(pc.destination))


if __name__ == '__main__':
    unittest.main()