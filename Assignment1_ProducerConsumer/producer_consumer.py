import threading
import queue
import time

class ProducerConsumer:
    """
    Producer-Consumer pattern using thread-safe queue.
    Producer adds items to queue, Consumer removes and processes them.
    """
    
    def __init__(self, source_data, queue_capacity=3):
        """
        Initialize the system with source data and queue size.
        """
        self.source = list(source_data)
        self.destination = []
        self.shared_queue = queue.Queue(maxsize=queue_capacity)
        self.producer_thread = None
        self.consumer_thread = None
        self.output_file = "outputs/producer_consumer_output.txt"
    
    def log(self, message):
        """Print to console and save to file."""
        print(message)
        with open(self.output_file, 'a') as f:
            f.write(message + '\n')
    
    def producer(self):
        """
        Producer: reads from source and puts items into queue.
        Blocks automatically when queue is full (wait mechanism).
        """
        self.log("Producer: Starting to produce items")
        
        for item in self.source:
            self.log(f"Producer: Adding {item} to queue")
            self.shared_queue.put(item)  # Blocks if queue is full
            self.log(f"Producer: Successfully added {item} (Queue size: {self.shared_queue.qsize()})")
            time.sleep(0.5)  # Simulate work
        
        self.log("Producer: Finished producing all items")
    
    def consumer(self):
        """
        Consumer: gets items from queue and stores in destination.
        Blocks automatically when queue is empty (wait mechanism).
        """
        self.log("Consumer: Starting to consume items")
        
        for _ in range(len(self.source)):
            self.log("Consumer: Trying to get item from queue")
            item = self.shared_queue.get()  # Blocks if queue is empty
            self.log(f"Consumer: Got {item} from queue")
            
            self.destination.append(item)
            self.shared_queue.task_done()  # Notify that item was processed
            
            self.log(f"Consumer: Stored {item} in destination (Total: {len(self.destination)})")
            time.sleep(1)  # Simulate work (slower than producer)
        
        self.log("Consumer: Finished consuming all items")
    
    def start(self):
        """
        Start producer and consumer threads, wait for completion.
        """
        # Create output directory
        import os
        os.makedirs('outputs', exist_ok=True)
        
        # Clear previous output file
        with open(self.output_file, 'w') as f:
            f.write("=== PRODUCER-CONSUMER PATTERN OUTPUT ===\n\n")
        
        self.log(f"Source data: {self.source}")
        self.log(f"Queue capacity: {self.shared_queue.maxsize}\n")
        
        # Create and start threads
        self.producer_thread = threading.Thread(target=self.producer, daemon=True)
        self.consumer_thread = threading.Thread(target=self.consumer, daemon=True)
        
        self.producer_thread.start()
        self.consumer_thread.start()
        
        # Wait for both threads to complete
        self.producer_thread.join()
        self.consumer_thread.join()
        self.shared_queue.join()
        
        self.log(f"\n=== COMPLETE ===")
        self.log(f"Final destination: {self.destination}")
        self.log(f"Items processed: {len(self.destination)}")
        self.log(f"Success: {self.source == self.destination}")
        
        print(f"\n✓ Output saved to: {self.output_file}")


if __name__ == "__main__":
    # Run with sample data
    source_data = [1, 2, 3, 4, 5, 6, 7, 8]
    pc_system = ProducerConsumer(source_data, queue_capacity=3)
    pc_system.start()