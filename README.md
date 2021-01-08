Natural Neighbourhoods
======================

Fork of [City of Edinburgh Council survey data](https://github.com/edinburghcouncil/natural-neighbourhoods), with goal of visualising natural neighbourhoods. Main developments:

* Geocoded postcodes with lat-long coordinates
* Expanded neighbourhoods of the form 'X/Y/Z' into constituents (and replicating the rest of the row)
* Aggregated some specialised neighbourhoods into super-areas; e.g. 'West Pilton' -> 'Pilton'
* Ignored neighbourhoods containing fewer than 10 points, and generic terms like 'East Edinburgh'. The original 264 terms are reduced to 72.

This [map](https://ewan.carto.com/viz/0bfeea56-af6d-11e6-baba-0e3ff518bd15/public_map) is one of my attempts to visualise the survey data. Points corresponding to postcodes are coloured according to their natural neighbourhood classification. The map illustrates the lack of clear boundaries between neighbourhoods and offers an interesting insight into [vernacular geography](https://en.wikipedia.org/wiki/Vernacular_geography).

You can compare this with the [CEC map of natural neighbourhoods](https://data.edinburghcouncilmaps.info/datasets/4082b44746eb4da8b5935be2d3a00185_27), which assigns sharp boundaries for administrative convenience. 
