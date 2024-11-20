from bs4 import BeautifulSoup
import requests

# URL target for scraping
print("Masukkan url yang mau di crawling atau scraping : ")
url = input()  # Replace with the actual URL


def scrape_filtered_content(url):
    try:
        # Send HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the status code is not 200

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Get the title
        title = soup.find("title")  # Replace with the appropriate tag for the title
        title_text = title.get_text(strip=True) if title else "No title found"

        # Get all <p> elements
        p_elements = soup.find_all("p")

        # Filter out unwanted content
        unwanted_phrases = ["ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT"]
        body = [
            p.get_text(strip=True)
            for p in p_elements
            if p.get_text(strip=True) not in unwanted_phrases
            and len(p.get_text(strip=True)) > 0
        ]

        # Return the results
        results = {"title": title_text, "body": body}
        return results

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def save_to_file(data, filename="output.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            # Write title
            file.write(f"{data['title']}\n\n")

            # Write body paragraphs
            for paragraph in data["body"]:
                file.write(f"{paragraph}\n\n")

        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Failed to save data: {e}")


# Execute the function
data = scrape_filtered_content(url)

# Save the output to a text file if data exists
if data:
    save_to_file(data)
else:
    print("No data found or an error occurred.")
