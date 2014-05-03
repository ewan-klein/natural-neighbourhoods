HTMLDIR := ../natural-neighbourhood-pages
INDEX-OUT := index.html
JS-OUT := ../natural-neighbourhood-pages/heatmap-data

CSV-IN := nn_data_normalised.csv
BUILDER := scripts/heatmap.py

ci: html jsdata
	cd $(HTMLDIR); git ci -m "Updated HTML" $(HTML-OUT); git push

html: jsdata
	python $(BUILDER) $(CSV-IN) $(HTMLDIR)/$(HTML-OUT)

jsdata: $(CSV-IN)
	git ci -m "Updated CSV file" $<; git push



