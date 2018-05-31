# Google Maps Muti-Route Calculator

Generates time and distance data from one source to many destinations or many destinations to one source.

## Getting Started

1. Create a CSV without a header that contains a list of either sources or destinations.
2. Install Selenium.
3. Run the script from the terminal.

### Prerequisites

Selenium
```
pip install selenium
```

### Running

Sources/Destinations values can be anything that's accepted by the Google Maps search boxes.
```
"Home"
"That Restaurant"
"1600 Amphitheatre Parkway, Mountain View, CA 94043"
```

From one source to many destinations
```
python3 multi_router.py "Source" "Destination.csv"
```

From many sources to one destination
```
python3 multi_router.py "Source.csv" "Destination"
```

End with an example of getting some data out of the system or using it for a little demo

## Built With
* [Python 3.6](https://www.python.org/downloads/)
* [Selenium](https://seleniumhq.github.io/selenium/docs/api/py/) - The web scraper used

## Authors

* **Albert Lam** - *All the work* - [simplyalam](https://github.com/simplyalam)

## License

This project is licensed under the GPL License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to Selenium for building an amazing web scraper
* Thanks to Google for providing a quick and easy to automate maps service
