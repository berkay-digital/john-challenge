# Web Scraper
This project is a web scraper that extracts product data from a website. It made for John Rooney's basic web scraping challenge.

## Files
- `main.py`: This is the main Python script that handles the web scraping.
- `products.csv`: This is the CSV file where the scraped product data is stored.

## How it Works
The `main.py` script uses the `requests` and `BeautifulSoup` libraries to scrape data from the website. It sends a GET request to the website, parses the HTML response to find product links, and then stores these links for further processing.

## Usage
To use this project, you need to have Python installed on your system. The main script is `main.py`, which can be run from the command line.

```sh
python main.py
```

## Dependencies
You can install dependencies using pip:
```sh
pip install requests beautifulsoup4 pandas
```

## Contributing
Contributions are welcome. Please open an issue to discuss your idea or submit a Pull Request.

## License
This project is licensed under the terms of the MIT license.