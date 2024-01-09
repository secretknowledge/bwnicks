# API Key = 3ae7e469-f78e-474e-9d0c-1ee6c4378127

"""
TODO:

- Add error message when API is rate limited / disabled / out of requests.
- Optimise caching format for performance and so it doesn't take up too much space.
- Create custom class alike to SimpleNamespace that is more memory efficient and more optimised toward our data.
- Other random optimisation.
- Add more custom error handling.
- Reorganise code and split into separate files.
- Fix latest.log parsing to not be a memory leak.
- Make thread safe.
- Make asynchronous.
- User Interface
    - Add a option for refreshing player data every 30 minutes seconds or leaving it to be removed after a week.
    - Periodically refresh player data
    - Periodically scan latest.log file for new data
    - Add options to clear logs, disable logs, and change loging level.
    - Add option to clear cache and disable cache.
    - Loading animations
"""
