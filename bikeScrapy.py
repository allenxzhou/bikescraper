# UI Prompt for Bike Scrapy

#import bikes
#import openBikes
import re
import requests
import sys

class BikeScrapy:

    def __init__(self, brand='Trek', size='52', shifters='Ultegra'):
        self.brand = brand
        self.size = size
        self.shifters = shifters
        self.options = {'y': '',
                        'o': '',
                        's': '',
                        'n': lambda: None}

    def search(self):
        return False

    def url_action(self, option):
        return False


if __name__ == "__main__":
    print "Press CTRL+C at any time to exit."
    promptFeature = lambda feature: raw_input(feature + '\n>>> ')
    
    while True:
        try:
            print "*Currently customized primarily for road bikes"
            brand = promptFeature('BRAND')
            size = promptFeature('SIZE')
            shifters = promptFeature('SHIFTERS')
            print "Generating URLs..."
            bike_scrapy = BikeScrapy(brand, size, shifters)

            while True:
                option = promptFeature('URLs: Open/Save? ' +
                    r"(Options = 'y', 'o', 's', 'n')")

                if option in bike_scrapy.options:
                    bike_scrapy.options[option]
                    break
                else:
                    print(r"Please enter 'y', 'o', 's', or 'n'")
        except KeyboardInterrupt:
            sys.exit('\nExiting...\n')
