#!/usr/bin/env python

""" Utility to find the distance and time from location(s) to location(s)

    Generate one source to many destinations:
        Ex. $ ./multi_router.py "source" destination.csv"
    Generate many sources to one destination:
        Ex. $ ./multi_router.py "source.csv" "destination"
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import sys

Browser = webdriver.chrome.webdriver.WebDriver

__author__ = 'Albert Lam'

__license__ = 'GPL'
__version__ = '1.0.0'

GOOGLE_MAPS = 'https://www.google.com/maps/dir/'
WAIT_TIME = 10


def find_many_to_one(csv_name: str, src_name: str) -> None:
    find_one_to_many(csv_name, src_name, True)


def find_one_to_many(src_name: str, csv_name: str, src_many=False) -> None:
    """Retrieves distance and time from one source to many locations.

    Args:
        src_name: the destination name/address.
        csv_name: the automated browser.
        src_many: True if finding many to one, False if finding one to many.

    """

    if src_many:
        src_name, csv_name = csv_name, src_name

    print('Starting Chrome Browser . . .')
    browser = webdriver.Chrome()
    browser.get(GOOGLE_MAPS)
    if not fill_search_box(src_name, browser, not src_many):
        print('Failed to fill destination box.') if src_many else print('Failed to fill source box.')
        return

    print(f'Reading sources from {csv_name}.') if src_many else print(f'Reading destinations from {csv_name}.')
    with open(csv_name, 'r') as src_csv_file:
        reader = csv.reader(src_csv_file)
        dest_csv_name = f'{csv_name[:-4]}_dist_time.csv'

        print(f'Writing results to {dest_csv_name}.')
        with open(dest_csv_name, 'w') as dest_csv_file:
            writer = csv.writer(dest_csv_file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(['locations', 'distance_mi', 'time_min'])

            # Iterates through each destination in the CSV
            for dest_name in iter(reader):
                dest_name = str(dest_name[0])
                distance, travel_time = find_dist_time(dest_name, browser, src_many)

                # Converts the distance and time to numerical values.
                if distance is not None and travel_time is not None:
                    distance = float(distance.split()[0])
                    t_split = travel_time.split()
                    travel_time = int(t_split[0])
                    if t_split[1] == 'h':
                        travel_time *= 60
                    if len(t_split) == 4:
                        travel_time += int(t_split[2])

                print(f'{dest_name}, {distance}, {travel_time}')
                writer.writerow([dest_name, distance, travel_time])
    print('Finished!')


def fill_search_box(name: str, browser: Browser, is_src) -> bool:
    """Attempts to fill the source box in Google Maps.

    Args:
        name: The source/destination name.
        browser: The automated browser.
        is_src: True if name is source, False if name is destination.
    Returns:
        The return value. True if source box is filled, False otherwise.

    """

    try:
        WebDriverWait(browser, WAIT_TIME)\
            .until(ec.presence_of_element_located((By.CLASS_NAME, 'tactile-searchbox-input')))
        if is_src:
            search_box = browser.find_elements_by_class_name('tactile-searchbox-input')[0]
        else:
            search_box = browser.find_elements_by_class_name('tactile-searchbox-input')[1]
        search_box.clear()
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN)
    except TimeoutException:
        print('Failed to find search boxes.')
        return False
    return True


def find_dist_time(dest_name: str, browser: Browser, src_many) -> (str, str):
    """Attempts to fill destination box and retrieve the distance and time.

    Args:
        dest_name: The destination name/address.
        browser: The automated browser.
        src_many: True is finding many to one, False if finding one to many.
    Returns:
        The return value. First is distance, second is time.

    """

    fill_search_box(dest_name, browser, src_many)

    # Attempts to retrieve the distance and travel time
    distance, travel_time = None, None
    try:
        trip_block = WebDriverWait(browser, WAIT_TIME)\
            .until(ec.presence_of_element_located((By.ID, 'section-directions-trip-0')))
        trip_values = trip_block.find_element_by_class_name('section-directions-trip-numbers')
        distance = trip_values.find_element_by_class_name('section-directions-trip-distance').text
        travel_time = trip_values.find_element_by_class_name('section-directions-trip-duration').text
    except TimeoutException:
        try:
            browser.find_element_by_class_name('section-directions-error-primary-text')
        except NoSuchElementException:
            print('Loading took too long!')
        else:
            print('Destination is unreachable!')
    return distance, travel_time


if __name__ == '__main__':
    if sys.argv[1][-4:] == '.csv':
        find_many_to_one(sys.argv[1], sys.argv[2])
        pass
    else:
        find_one_to_many(sys.argv[1], sys.argv[2])
