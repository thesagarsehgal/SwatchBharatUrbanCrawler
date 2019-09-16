from setuptools import setup, find_packages

setup(
    name         = 'swatchbharaturban_crawler',
    version      = '1.0',
    packages     = find_packages(where=""),
    entry_points = {'scrapy': ['settings = swatchbharaturban_crawler.settings']},
)