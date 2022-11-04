## Pure django API

**Endpoints:**

1. **api/v1/genres/** *(no parameters)*
2. **api/v1/movies/** *(**genre**=Filter out movies that do not have the specified genre. You need to provide genre id. **src**=Filter out movies, that doesn't match specified search phase. **page**=Splits the data into pages and returns one of them. The number of objects on the page is controlled in the ITEMS_PER_PAGE variable in the views.py file)*
3. **api/v1/movies/**<movie_id>