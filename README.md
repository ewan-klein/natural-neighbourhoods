Natural Neighbourhoods
======================

Fork of [City of Edinburgh Council survey data](https://github.com/edinburghcouncil/natural-neighbourhoods), with goal of visualising natural neighbourhoods. Main developments:

* Geocoded postcodes with lat-long
* Expanded neighbourhoods of the form 'X/Y/Z' into constituents (and replicating the rest of the row)
* Aggregated some specialised neighbourhoods into super-areas; e.g. 'West Pilton' -> 'Pilton'
* Ignored neighbourhoods containing fewer than 10 points, and generic terms like 'East Edinburgh'. The original 264 terms are reduced to 72.

This [map](https://ewan.carto.com/viz/0bfeea56-af6d-11e6-baba-0e3ff518bd15/public_map) is an attempt to visualise the survey data. Points corresponding to postcodes are coloured according to the natural neighbourhood classification. The map illustrates the lack of clear boundaries between neighbourhoods.
