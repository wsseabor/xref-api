TODO:

    ~~Include try/catch with error logging for SessionNotCreatedException, TimeoutException in individual
    calls to each class that handles scraping (app/scrapers)~~ DONE

    ~~Circular dependency issue~~ DONE

    Finish classes for all separate stats tables

    ~~Find the correct xpath expression that does not include final rows in certain tables (pp36 awards column)~~ DONE
        -CSS selector is the way to go

    Make main function utilize command line, function more "API-like"

    Error logging class?

    Update / install chromedriver on launch (may switch to playwright at later date for browser pools &c. )

    Refactor classes

        - Selenium class to init all boilerplate in one instead of repeating through every class (DRY?)
        - Refactor all scrape classes to stick with DRY as well?

    
