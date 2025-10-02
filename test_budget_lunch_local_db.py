import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import json

# Add the current directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app and functions
from budget_lunch_local_db import app, search_food_with_price, add_food_item, lunch_db

class TestBudgetLunchLocalDB(unittest.TestCase):
    """Comprehensive unit tests for budget_lunch_local_db.py"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Store the original lunch_db to restore it after tests
        self.original_lunch_db = lunch_db.copy()
        
        # Create a test client for Flask app testing
        self.app = app.test_client()
        self.app.testing = True
    
    def tearDown(self):
        """Clean up after each test method"""
        # Restore the original lunch_db
        lunch_db.clear()
        lunch_db.extend(self.original_lunch_db)

    # ==================== SEARCH_FOOD_WITH_PRICE TESTS ====================
    
    def test_search_exact_price_match(self):
        """Test searching for items with exact price match"""
        result = search_food_with_price(6.99)
        # Should return pizza and all items <= 6.99
        self.assertEqual(len(result), 4)
        names = [item["name"] for item in result]
        self.assertIn("pizza", names)
        for item in result:
            self.assertLessEqual(item["price"], 6.99)
    
    def test_search_lower_price(self):
        """Test searching for items under a lower price"""
        result = search_food_with_price(3.00)
        self.assertEqual(len(result), 2)
        names = [item["name"] for item in result]
        self.assertIn("soda", names)
        self.assertIn("coffee", names)
        for item in result:
            self.assertLessEqual(item["price"], 3.00)
    
    def test_search_very_low_price(self):
        """Test searching with a very low price (should return no results)"""
        result = search_food_with_price(1.00)
        self.assertEqual(len(result), 0)
    
    def test_search_high_price(self):
        """Test searching with a high price (should return all items)"""
        result = search_food_with_price(10.00)
        self.assertEqual(len(result), 4)
        names = [item["name"] for item in result]
        expected_names = ["pizza", "salad", "soda", "coffee"]
        for name in expected_names:
            self.assertIn(name, names)
    
    def test_search_boundary_price(self):
        """Test searching with boundary price values"""
        result = search_food_with_price(2.99)
        self.assertEqual(len(result), 2)
        names = [item["name"] for item in result]
        self.assertIn("soda", names)
        self.assertIn("coffee", names)
    
    def test_search_with_string_price(self):
        """Test that function handles string input correctly"""
        result = search_food_with_price("5.99")
        self.assertEqual(len(result), 3)
        names = [item["name"] for item in result]
        self.assertIn("salad", names)
        self.assertIn("soda", names)
        self.assertIn("coffee", names)
        self.assertNotIn("pizza", names)
    
    def test_search_with_zero_price(self):
        """Test searching with zero price"""
        result = search_food_with_price(0)
        self.assertEqual(len(result), 0)
    
    def test_search_with_negative_price(self):
        """Test searching with negative price"""
        result = search_food_with_price(-1.0)
        self.assertEqual(len(result), 0)
    
    def test_search_decimal_precision(self):
        """Test searching with decimal precision"""
        result = search_food_with_price(5.50)
        self.assertEqual(len(result), 2)
        names = [item["name"] for item in result]
        self.assertIn("soda", names)
        self.assertIn("coffee", names)
        self.assertNotIn("salad", names)
    
    def test_search_result_structure(self):
        """Test that returned items have the correct structure"""
        result = search_food_with_price(10.00)
        for item in result:
            self.assertIn("name", item)
            self.assertIn("price", item)
            self.assertIn("imageurl", item)
            self.assertIsInstance(item["price"], (int, float))
            self.assertIsInstance(item["name"], str)
            self.assertIsInstance(item["imageurl"], str)

    # ==================== ADD_FOOD_ITEM TESTS ====================
    
    def test_add_food_item_basic(self):
        """Test adding a basic food item"""
        initial_count = len(lunch_db)
        response = self.app.get('/add/burger/8.99')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        self.assertEqual(len(lunch_db), initial_count + 1)
        self.assertEqual(lunch_db[-1]["name"], "burger")
        self.assertEqual(lunch_db[-1]["price"], 8.99)
        self.assertIsNone(lunch_db[-1]["imageurl"])
    
    def test_add_food_item_with_image(self):
        """Test adding a food item with image URL"""
        initial_count = len(lunch_db)
        response = self.app.get('/add/burger/8.99?imageurl=https://example.com/burger.jpg')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        self.assertEqual(len(lunch_db), initial_count + 1)
        self.assertEqual(lunch_db[-1]["imageurl"], "https://example.com/burger.jpg")
    
    def test_add_food_item_with_decimal_price(self):
        """Test adding item with decimal price"""
        response = self.app.get('/add/sandwich/7.50')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        self.assertEqual(lunch_db[-1]["price"], 7.50)
    
    def test_add_food_item_with_string_price(self):
        """Test adding item with string price (should convert to float)"""
        response = self.app.get('/add/fries/3.25')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        self.assertEqual(lunch_db[-1]["price"], 3.25)
        self.assertIsInstance(lunch_db[-1]["price"], float)
    
    def test_add_food_item_with_zero_price(self):
        """Test adding item with zero price"""
        response = self.app.get('/add/free_sample/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        self.assertEqual(lunch_db[-1]["price"], 0)
    
    def test_add_food_item_with_negative_price(self):
        """Test adding item with negative price"""
        response = self.app.get('/add/discount_item/-1.50')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        self.assertEqual(lunch_db[-1]["price"], -1.50)
    
    def test_add_food_item_with_special_characters(self):
        """Test adding item with special characters in name"""
        response = self.app.get('/add/café_latte/4.25')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        self.assertEqual(lunch_db[-1]["name"], "café_latte")
    
    def test_add_food_item_with_empty_name(self):
        """Test adding item with empty name"""
        # Use URL encoding for empty string
        response = self.app.get('/add/%20/5.00')  # Space character
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        self.assertEqual(lunch_db[-1]["name"], " ")
    
    def test_add_food_item_with_very_long_name(self):
        """Test adding item with very long name"""
        long_name = "a" * 1000
        response = self.app.get(f'/add/{long_name}/10.00')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        self.assertEqual(lunch_db[-1]["name"], long_name)
    
    def test_add_food_item_multiple_times(self):
        """Test adding multiple items sequentially"""
        initial_count = len(lunch_db)
        
        self.app.get('/add/item1/1.00')
        self.app.get('/add/item2/2.00')
        self.app.get('/add/item3/3.00')
        
        self.assertEqual(len(lunch_db), initial_count + 3)
        self.assertEqual(lunch_db[-3]["name"], "item1")
        self.assertEqual(lunch_db[-2]["name"], "item2")
        self.assertEqual(lunch_db[-1]["name"], "item3")

    # ==================== FLASK ROUTE TESTS ====================
    
    def test_home_route(self):
        """Test the home route returns index.html"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
    
    def test_search_route_valid_price(self):
        """Test the search route with valid price"""
        response = self.app.get('/search/5.00')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
    
    def test_search_route_zero_price(self):
        """Test the search route with zero price"""
        response = self.app.get('/search/0')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 0)
    
    def test_search_route_negative_price(self):
        """Test the search route with negative price"""
        response = self.app.get('/search/-5')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 0)
    
    def test_search_route_decimal_price(self):
        """Test the search route with decimal price"""
        response = self.app.get('/search/3.50')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
    
    def test_add_route_basic(self):
        """Test the add route with basic parameters"""
        response = self.app.get('/add/test_item/5.99')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
    
    def test_add_route_with_image(self):
        """Test the add route with image URL parameter"""
        response = self.app.get('/add/test_item/5.99?imageurl=https://example.com/image.jpg')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
    
    def test_add_route_decimal_price(self):
        """Test the add route with decimal price"""
        response = self.app.get('/add/decimal_item/7.25')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
    
    def test_styles_css_route(self):
        """Test the styles.css route"""
        response = self.app.get('/styles.css')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/css; charset=utf-8')
    
    def test_script_js_route(self):
        """Test the script.js route"""
        response = self.app.get('/script.js')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/javascript; charset=utf-8')

    # ==================== INTEGRATION TESTS ====================
    
    def test_search_after_add_integration(self):
        """Test searching after adding new items"""
        # Add a new item
        self.app.get('/add/new_pizza/4.99?imageurl=https://example.com/pizza.jpg')
        
        # Search for items under $5
        response = self.app.get('/search/5.00')
        data = response.get_json()
        
        # Should include the new item
        names = [item["name"] for item in data]
        self.assertIn("new_pizza", names)
    
    def test_multiple_adds_and_search(self):
        """Test adding multiple items and searching"""
        # Add multiple items
        self.app.get('/add/cheap_burger/3.99')
        self.app.get('/add/expensive_steak/15.99')
        self.app.get('/add/mid_pasta/8.50')
        
        # Search under $10
        response = self.app.get('/search/10.00')
        data = response.get_json()
        names = [item["name"] for item in data]
        
        self.assertIn("cheap_burger", names)
        self.assertIn("mid_pasta", names)
        self.assertNotIn("expensive_steak", names)
    
    def test_search_with_original_data(self):
        """Test that original data is preserved and searchable"""
        response = self.app.get('/search/10.00')
        data = response.get_json()
        names = [item["name"] for item in data]
        
        # Should include original items
        self.assertIn("pizza", names)
        self.assertIn("salad", names)
        self.assertIn("soda", names)
        self.assertIn("coffee", names)
    
    def test_add_with_special_characters(self):
        """Test adding items with special characters in URL"""
        special_name = "café_&_restaurant"
        response = self.app.get(f'/add/{special_name}/6.50')
        self.assertEqual(response.status_code, 200)
        
        # Verify it was added
        search_response = self.app.get('/search/10.00')
        data = search_response.get_json()
        names = [item["name"] for item in data]
        self.assertIn(special_name, names)
    
    def test_error_handling_invalid_price(self):
        """Test error handling for invalid price format"""
        response = self.app.get('/search/invalid_price')
        # Should return 500 error for invalid price format
        self.assertEqual(response.status_code, 500)
    
    def test_large_price_search(self):
        """Test searching with very large price"""
        response = self.app.get('/search/999999.99')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # Should return all items
        self.assertEqual(len(data), len(self.original_lunch_db))
    
    def test_precision_price_search(self):
        """Test searching with high precision decimal"""
        response = self.app.get('/search/2.999')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # Should include items with price <= 2.999
        for item in data:
            self.assertLessEqual(item["price"], 2.999)
    
    def test_empty_search_results(self):
        """Test search that returns no results"""
        response = self.app.get('/search/0.50')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 0)
    
    def test_add_item_persistence(self):
        """Test that added items persist during the session"""
        # Add an item
        self.app.get('/add/persistent_item/9.99')
        
        # Search for it
        response = self.app.get('/search/10.00')
        data = response.get_json()
        names = [item["name"] for item in data]
        self.assertIn("persistent_item", names)
        
        # Search again to ensure persistence
        response2 = self.app.get('/search/10.00')
        data2 = response2.get_json()
        names2 = [item["name"] for item in data2]
        self.assertIn("persistent_item", names2)

if __name__ == '__main__':
    # Run the tests with verbose output
    unittest.main(verbosity=2)
