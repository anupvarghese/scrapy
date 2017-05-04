## Web scraping using Scrapy

Use scrapy to get Aviation data from Aviation Safety Network for analytical purposes

### How to run

```shell
docker-compose run scrapy bash
cd safety
scrapy crawl aviation -o output.csv
```

### Preview

|                                                                                                                                                                                                                                                                                                                                          |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Passengers,OperatedBy,Engines,CrashSiteElevation,Operator,OperatingFor,FlightNumber,Crew,Phase,Location,Time,Cycles,Type,GroundCasualities,TotalFatalities,TotalAirFrameHrs,Nature,DestinationAirport,AirplaneDamage,CarrierNumber,Registration,Date,DepartureAirport,AirplaneFate,CollisionCasualties,FirstFlight                       |
| Fatalities: 0 / Occupants: 9,-,2,-,KLM Royal Dutch Airlines,-,-,Fatalities: 1 / Occupants: 2,En route (ENR),United Kingdom / St. Julians# Sevenoaks# Kent,ca 08:15,-,Fokker F.VIII,-,Fatalities: 1 / Occupants: 11,,International Scheduled Passenger,-,Damaged beyond repair,4993,H-NADU,Monday 22 August 1927,# United Kingdom,,-,1926 |
