# simple-crawler

A super simple webcrawler framework written in Python.

## Brief overview of architecture
- The crawler is based on a configurable [workerpool](https://github.com/shazow/workerpool). There can only be N worker threads at any given time. These worker threads are then responsible for grabing jobs if they are free. If no workers are fee, jobs would be queued to be processed later. This kind of architecture allows us to make asynchrnous IO possible without exhausting system resources.
- The Python class `SimpleCrawler` is an exhaustive crawler implementation which would keep on discovering links and crawling them until it has seen every link.
- Current implementation of crawler is stateless (No support to pause or resume crawling).
- Uses xpath to extract absolute and relative urls in a document.
- Separates out data cleaning and saving into **collectors** and **post processors**.
- **Collectors** are callbacks to clean a parsed item. These callbacks are *chained* so a cleaned item would go from one collector to another in the chain.
- **Post processor** is where you would do all data IO. There can be multiple post processors such that one can save data to file and another can save data to a DB.
- The whole crawling process is written to stdout.

## Techniques:
- Uses hashing to skip duplicate urls for a single uninterrupted run.
- Uses `threading.Lock()` to avoid race conditions on modification to url hashes set.

## Project layout
The project contains:

- dir `webcrawler`: This contains the basic framework implementation.
- dir `example`: Contains an example that implements a spider to extract all static assets from [dubai.dubizzle.com](dubai.dubizzle.com) and save it to a file.

## Setting up the project
- Extract the archive.
- `cd` into the project directory.
- [OPTIONAL] Create a virtualenv for the directory and activate it. 
- do `export PYTHONPATH=$PWD`
- do `pip install -r requirements/development.txt`

## Running the example
- Open two shells.
- Issue `python example/run.py > run.log` to start scraping [dubai.dubizzle.com](dubai.dubizzle.com).
- Tail the logs on the other shell.
- To stop the crawler, issue `pkill -f example/run.py`. `Ctrl-C` won't work so `pkill` is the recommended way.
- Once you are done with scraping or you forced an exit, you can see the html sitemap files in the result folder.

## Tests
- To run mock tests, issue the command `nosetests` from the project dir.