import os
import re
import requests
import socket
from bs4 import BeautifulSoup


def is_valid_url(url):
    """Checks if a given string is a valid URL or IP address."""
    try:
        result = socket.getaddrinfo(url, None)
        return True
    except:
        return False


def get_links(url, timeout):
    """Gets all the links from a given URL."""
    try:
        response = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, "html.parser")
        links = [link.get("href") for link in soup.find_all("a")]
        return links
    except:
        return []


def check_link(link, timeout):
    """Checks if a given link is dead."""
    try:
        response = requests.get(link, timeout=timeout)
        if response.status_code >= 400:
            return link
    except:
        return link


def save_to_txt(dead_links, file_path):
    """Saves the dead links to a text file."""
    with open(file_path, "w") as f:
        f.write("\n".join(dead_links))


def save_to_xml(dead_links, file_path):
    """Saves the dead links to an XML file."""
    with open(file_path, "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<dead_links>\n")
        for link in dead_links:
            f.write(f"  <link>{link}</link>\n")
        f.write("</dead_links>")


if __name__ == "__main__":
    url_or_ip = input("Enter the URL or IP address to check for dead links: ")
    timeout = 100

    print(f"Getting links from {url_or_ip}...")
    links = get_links(url_or_ip, timeout)
    print(f"Found {len(links)} links.")

    print("Checking links...")
    dead_links = [check_link(link, timeout) for link in links]
    dead_links = [link for link in dead_links if link is not None]
    print(f"Found {len(dead_links)} dead links.")

    # Save results in both formats automatically
    file_name = "dead_links"
    if len(dead_links) > 0:
        save_to_txt(dead_links, f"{file_name}.txt")
        save_to_xml(dead_links, f"{file_name}.xml")
        print(f"Dead links saved in {file_name}.txt and {file_name}.xml")
    else:
        print("No dead links found.")
