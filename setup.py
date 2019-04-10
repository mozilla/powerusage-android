from setuptools import setup

setup(
    name = "powerusage-android",
    version = "0.1.0",
    author = "Mozilla",
    author_email = "gmierz1@live.ca",
    description = ("Tools for testing power usage on Android devices. "),
    license = "MPL",
    keywords = "Android power and battery usage",
    url = "https://github.com/mozilla/powerusage-android",
    packages=[
        'utils',
        'tests',
    ],
    classifiers=[
        "Development Status :: Beta",
    ]
)
