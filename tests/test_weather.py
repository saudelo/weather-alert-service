#!/usr/bin/env python3
"""
Simple unit tests for test-project.py
"""

import unittest
from unittest.mock import patch, Mock
import sys
from io import StringIO

# Import your script
import importlib.util
spec = importlib.util.spec_from_file_location("test_project", "test-project.py")
test_project = importlib.util.module_from_spec(spec)
sys.modules["test_project"] = test_project
spec.loader.exec_module(test_project)


class SimpleWeatherTests(unittest.TestCase):
    """Simple tests for the weather monitoring script."""
    
    @patch('test_project.requests.get')
    def test_successful_request(self, mock_get):
        """Test 1: Normal working request with total alerts."""
        # Create a fake successful response
        fake_response = Mock()
        fake_response.json.return_value = {'total': 5}
        mock_get.return_value = fake_response
        
        # Capture what gets printed
        captured = StringIO()
        sys.stdout = captured
        
        # Run the function
        test_project.get_active_alerts()
        
        # Put stdout back to normal
        sys.stdout = sys.__stdout__
        
        # Check the output
        output = captured.getvalue()
        self.assertIn('Total 5 active alerts', output)
    
    @patch('test_project.requests.get')
    def test_missing_total(self, mock_get):
        """Test 2: What happens when 'total' is missing from response."""
        # Create a fake response WITHOUT 'total'
        fake_response = Mock()
        fake_response.json.return_value = {}
        mock_get.return_value = fake_response
        
        # Capture what gets printed
        captured = StringIO()
        sys.stdout = captured
        
        # Run the function
        test_project.get_active_alerts()
        
        # Put stdout back to normal
        sys.stdout = sys.__stdout__
        
        # Check it shows N/A
        output = captured.getvalue()
        self.assertIn('Total N/A active alerts', output)
    
    @patch('test_project.requests.get')
    def test_network_error(self, mock_get):
        """Test 3: What happens when network request fails."""
        # Make the request fail with a timeout
        mock_get.side_effect = test_project.requests.exceptions.Timeout("Connection timeout")
        
        # Capture what gets printed
        captured = StringIO()
        sys.stdout = captured
        
        # Run the function
        test_project.get_active_alerts()
        
        # Put stdout back to normal
        sys.stdout = sys.__stdout__
        
        # Check it shows an error message
        output = captured.getvalue()
        self.assertIn('Error fetching alerts', output)


if __name__ == '__main__':
    # Run the tests with verbose output
    unittest.main(verbosity=2)