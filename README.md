# Python SQLite Caching Utility

This Python script provides a simple utility for caching data using SQLite. It allows you to efficiently store and retrieve data associated with specific URLs.

## Dependencies
- Python 3.x
- SQLite3

## Usage
1. Import the required modules:
    ```python
    from caching_util import cache_data, get_data
    ```

2. Cache data using the `cache_data(url, data)` function:
    ```python
    url = "example.com"
    data = {"key": "value"}
    cache_data(url, data)
    ```

3. Retrieve cached data using the `get_data(url)` function:
    ```python
    # Retrieve the cached data
    cached_data = get_data(url)
    
    # Display the cached data
    print("Cached Data:", cached_data)
    ```

## Configuration
Ensure to configure the `config.py` file with appropriate settings, including the `CACHE_DAY` parameter for specifying the cache duration.

## Functions
- `cache_data(url, data)`: Caches data associated with a URL in the database.
- `get_data(url)`: Retrieves cached data associated with a URL from the database.

## Contributing
Feel free to contribute to this project by submitting pull requests or reporting issues.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
