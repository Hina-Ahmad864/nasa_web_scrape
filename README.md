# web-scraping-challenge

In jupyter notebook scraped and collected all items requried per instructions. Used pandas to gather table data, and put it into html code to paste into index.html.

Moved items from jupyter notebook file to `scrape_mars.py` to scrape requested information (title, paragraph, featured image, list of hemisphere urls) from the nasa page provided in the instruction. The `mars_data` function should return the requested material as a Python Dictionary (except for the list of hemisphere images).

In `app.py`, completed the `/scrape` route to store the Python dictionary as a document in a mongo database collection.

In `app.py`, completed the `/` route to read one entry from mongo and render the flask template with the mongo data.
