## Web scraping using Scrapy

Use scrapy to get Aviation data from Aviation Safety Network for analytical purposes

### How to run

```shell
docker-compose run scrapy bash
cd safety
scrapy crawl aviation -o output.csv
```
