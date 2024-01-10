import requests
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

baseurl = "https://gopher1.extrkt.com/"
product_links = []


def get_data(url):
    try:
        response = requests.get(url)
        data = response.text
        return data
    except requests.exceptions.ConnectionError as e:
        print(f"Failed to get data from {url}. Error: {e}")
        return None


def parser(data):
    soup = BeautifulSoup(data, "html.parser")
    return soup


def find_links(parsed_data):
    links = parsed_data.find_all(
        "a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link"
    )
    product_links = [link["href"] for link in links]
    return product_links


def info_scraper(url):
    data = get_data(url)
    parsed_data = parser(data)
    product_name = parsed_data.find("h1", class_="product_title entry-title").text
    product_price = parsed_data.find(
        "span", class_="woocommerce-Price-amount amount"
    ).text
    product_price = product_price.replace("$", "")
    product_price = product_price.replace("£", "")
    product_price = product_price.replace(",", "")
    product_price = float(product_price)
    product_image = parsed_data.find("img", class_="wp-post-image")["src"]
    product_description = parsed_data.find(
        "div",
        class_="woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab",
    ).text
    product_description = product_description.replace("Description", "")
    product_description = product_description.replace("\n", "")
    try:
        product_size = (
            parsed_data.find(
                "div",
                class_="woocommerce-Tabs-panel woocommerce-Tabs-panel--additional_information panel entry-content wc-tab",
            )
            .find(
                "tr",
                class_="woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_size",
            )
            .find("p")
            .text
        )
    except:
        product_size = "None."

    try:
        product_color = (
            parsed_data.find(
                "div",
                class_="woocommerce-Tabs-panel woocommerce-Tabs-panel--additional_information panel entry-content wc-tab",
            )
            .find(
                "tr",
                class_="woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_color",
            )
            .find("p")
            .text
        )
    except:
        product_color = "None."

    try:
        product_reviews = (
            parsed_data.find("div", class_="woocommerce-tabs wc-tabs-wrapper")
            .find("li", class_="reviews_tab")
            .text
        )
        product_reviews = product_reviews.replace("Reviews", "")
        product_reviews = product_reviews.replace("(", "")
        product_reviews = product_reviews.replace(")", "")
    except:
        product_reviews = "0"
    product_sku = parsed_data.find("span", class_="sku").text
    product_sku = product_sku.replace("SKU: ", "")
    product_category = parsed_data.find("span", class_="posted_in").find("a").text
    with open("products.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                product_name,
                product_price,
                product_image,
                product_description,
                product_size,
                product_color,
                product_reviews,
                product_sku,
                product_category,
            ]
        )
    return product_name


def main():
    start_time = time.time()
    global product_links
    data = get_data(baseurl)
    parsed_data = parser(data)
    page_numbers = parsed_data.select("ul.page-numbers")[0]
    last_page_number = page_numbers.find_all("li")[-2].text
    print("Page Numbers:", last_page_number)
    for i in range(1, int(last_page_number) + 1):
        url = baseurl + "?paged=" + str(i)
        data = get_data(url)
        parsed_data = parser(data)
        product_links.append(find_links(parsed_data))

    product_links = [item for sublist in product_links for item in sublist]

    print("Number of Products:", len(product_links))
    with open("products.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Product Name",
                "Product Price",
                "Product Image",
                "Product Description",
                "Product Size",
                "Product Color",
                "Product Reviews",
                "Product SKU",
                "Product Category",
            ]
        )

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(info_scraper, link) for link in product_links]
        for future in as_completed(futures):
            print("Product Scraped:", future.result())

    print("Scraping Completed")
    df = pd.read_csv("products.csv")
    df["Product Price"] = pd.to_numeric(df["Product Price"], errors="coerce")
    df = df.sort_values("Product Price", ascending=False)
    df.to_csv("products.csv", index=False)
    print("Sorting Completed")
    print("Time Taken:", time.time() - start_time, "seconds")


if __name__ == "__main__":
    main()
