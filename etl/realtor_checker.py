import requests
from bs4 import BeautifulSoup


URL = "https://www.realtor.com/research/data/"


def get_realtor_update_text():

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(URL, headers=headers, timeout=30)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    section = soup.find(
        "div",
        class_="monthly-inventory download-section"
    )

    if not section:
        raise ValueError(
            "Could not find monthly inventory section"
        )

    update_text = section.find(
        "p",
        class_="info"
    )

    if not update_text:
        raise ValueError(
            "Could not find update text"
        )

    return update_text.text.strip()


if __name__ == "__main__":
    print(get_realtor_update_text())
