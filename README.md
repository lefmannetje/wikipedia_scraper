# Wikipedia scraper

This is an excercise on how to scrape content from wikipedia.

For this excercise we used an API to get:
- cookies
- countries (codes: be, fr, ma, ru, etc...)
- leaders per country
- leader_id to get wikipedia webpage

After we got all the correct info we created a script that scraped each first paragraph for each leader. Then we stored all this information in a JSOn file called `leaders.json` 


## Deployment

To deploy this project run

```bash
  pip install -r /path/to/requirements.txt
  python main.py
```


## API Reference

#### info about used API

<a name="[unique-anchor-name](https://country-leaders.onrender.com/docs)">https://country-leaders.onrender.com/docs</a>


