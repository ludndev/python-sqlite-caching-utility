from caching_util import cache_data, get_data

# Sample data to cache
url = "example.com"
data = {"key": "value"}

# Cache the data
cache_data(url, data)

# Retrieve the cached data
cached_data = get_data(url)

# Display the cached data
print("Cached Data:", cached_data)
