# TrendSense Tests

This directory contains tests for the TrendSense application.

## Test Structure

- `test_routes.py`: Tests for the main application routes
- `test_tour_mode.py`: Tests for the TourMode feature
- `test_vc_lens_panels.py`: Tests for the VC Lens panels
- `js/`: JavaScript tests
  - `test_tour_mode.js`: Tests for the TourMode JavaScript functionality
  - `test_vc_lens_panels.js`: Tests for the VC Lens panels JavaScript functionality

## Running Tests

### Python Tests

To run the Python tests, use the following command:

```bash
python -m unittest discover tests
```

### JavaScript Tests

To run the JavaScript tests, use the following command:

```bash
npm test
```

### All Tests

To run all tests (both Python and JavaScript), use the following command:

```bash
python run_tests.py
```

## Writing Tests

### Python Tests

Python tests use the `unittest` framework. To create a new test file, follow these steps:

1. Create a new file in the `tests` directory with a name starting with `test_`.
2. Import the necessary modules:
   ```python
   import unittest
   import sys
   import os
   
   # Add the parent directory to the path
   sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
   
   from app import app
   ```
3. Create a test class that inherits from `unittest.TestCase`:
   ```python
   class TestMyFeature(unittest.TestCase):
       def setUp(self):
           """Set up test client."""
           self.app = app.test_client()
           self.app.testing = True
       
       def test_my_feature(self):
           """Test my feature."""
           # Test code here
   ```
4. Add test methods to the class. Each test method should start with `test_`.
5. Add a main block to allow running the test file directly:
   ```python
   if __name__ == '__main__':
       unittest.main()
   ```

### JavaScript Tests

JavaScript tests use the Jest framework. To create a new test file, follow these steps:

1. Create a new file in the `tests/js` directory with a name starting with `test_`.
2. Mock the necessary DOM elements:
   ```javascript
   document.body.innerHTML = `
   <div id="my-element"></div>
   `;
   ```
3. Import or mock the necessary JavaScript code.
4. Write test cases using Jest's `describe` and `test` functions:
   ```javascript
   describe('My Feature', () => {
     test('should do something', () => {
       // Test code here
       expect(something).toBe(somethingElse);
     });
   });
   ```
