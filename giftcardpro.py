import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

countries = {
    'Australia': 'AU',
    'Australia': 'AR',
    'Belgium': 'BE',
    'Brazil': 'BR',
    'Canada': 'CA',
    'Chile': 'CL',
    'Colombia': 'CO',
    'Czechia': 'CZ',
    'Denmark': 'DK',
    'Finland': 'FI',
    'France': 'FR',
    'Germany': 'DE',
    'Hungary': 'HU',
    'India': 'IN',
    'Ireland': 'IE',
    'Italy': 'IT',
    'Kenya': 'KE',
    'Malaysia': 'MY',
    'New Zealand': 'NZ',
    'Switzerland': 'CH',
    'United States': 'US',
    'United Kingdom': 'GB'
}


def remove_Files():

    for filename in ['mobileGift.txt', 'desktopGift.txt']:
        if os.path.exists(filename):
            os.remove(filename)


def display_country_list():

    print("Select a country from the list below:")
    for i, country in enumerate(countries.keys(), 1):
        print(f"{i}. {country}")


def get_user_selection():

    while True:
        try:
            selected_index = int(input("Enter the number corresponding to your country: ")) - 1
            if 0 <= selected_index < len(countries):
                selected_country = list(countries.keys())[selected_index]
                return countries[selected_country], selected_country
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_device_selection():

    while True:
        device = input("Enter the device mode (mobile/desktop): ").strip().lower()
        if device in ['mobile', 'desktop']:
            return device
        else:
            print("Invalid selection. Please enter 'mobile' or 'desktop'.")


def fetch_trending_topics(geo_code):

    url = f"https://trends.google.com/trends/trendingsearches/daily?geo={geo_code}&hl=en-US"
    driver = webdriver.Edge()
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    trending_topics = []
    trending_topics_divs = soup.find_all('div', class_='title')
    for div in trending_topics_divs:
        a_tags = div.find_all('a')
        for a in a_tags:
            topic_text = a.get_text(strip=True)
            if topic_text:
                trending_topics.append(topic_text)
    driver.quit()
    return trending_topics


def save_trending_topics(topics, filename):

    with open(filename, 'w') as file:
        for topic in topics:
            file.write(topic + '\n')
    print(f"Trending topics ({len(topics)} topics) have been saved to '{filename}'.")


def perform_search(file_path, device_mode):

    if device_mode == 'mobile':
        mobile_emulation = {"deviceName": "iPhone X"}
        options = Options()
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        driver = webdriver.Edge(options=options)
    else:
        driver = webdriver.Edge()

    driver.get("https://www.bing.com/")
    time.sleep(5)

    with open(file_path, 'r') as file:
        search_topics = file.readlines()

    for topic in search_topics:
        search_query = topic.strip()
        if search_query:
            if device_mode == 'mobile':
                search_box = driver.find_element(By.NAME, "q")
                search_box.clear()
                search_box.send_keys(search_query)
                search_box.send_keys(Keys.RETURN)
            else:
                driver.execute_script("document.getElementById('sb_form_q').value = '{}'".format(search_query))
                search_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "sb_form_go")))
                search_button.click()
            time.sleep(5)

    driver.quit()


def main():
    remove_Files()
    while True:
        print("**************************************************")
        print("*          Microsoft Reward Collector            *")
        print("**************************************************")
        display_country_list()
        geo_code, country = get_user_selection()
        device_mode = get_device_selection()
        trending_topics = fetch_trending_topics(geo_code)
        if device_mode == 'mobile':
            filename = 'mobileGift.txt'
        else:
            filename = 'desktopGift.txt'
        save_trending_topics(trending_topics, filename)
        print("Starting search process...")
        perform_search(filename, device_mode)
        print("Search process End.")
        restart = input("Do you want to start the program again or exit? (start/exit): ").strip().lower()
        if restart == 'exit':
            print("Thank You for Using Microsoft Reward Collector .")
            print("If you need any help contact +94717707903 .")
            break


if __name__ == "__main__":
    main()
