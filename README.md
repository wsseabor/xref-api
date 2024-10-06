Basketball reference API

A basketball reference webscraper factored out of an earlier repo. Integrate with
command line before shutteling back into the intial repo.

Many web scrapers for basketball reference are either outdated (7+ years!) or are not compatible with 
basketball reference as many stat lines they provide whether for teams or players are generated dynamically, 
so the usual option to stick with BeautifulSoup are not sufficient enough to tackle. This scraper utilizes Selenium 
to access a headless browser to allow dynamically scraped content to be packaged and used. Currently it is only for NBA 
but the future of this project will probably attempt to have most of the sports reference pages scrape-able.

Currently scrapes dynamic player stats from basketball reference and saves them in a pandas dataframe. 
Sample image is Damian Lillard's full season stats from rookie 2012 season to the current day. Can be
used for many other current season or past season stats.

![Dataframe image](/img/67813C0A-6A95-4D52-8F11-1CFF6D5C3764.jpeg)


