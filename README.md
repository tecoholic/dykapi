#DYKAPI

DYK API is s api which returns Did You Know hook data of the wikipedia. It gives the hook text (fact) and the related links.
As of now the code can genearte a random hook from the datastore and retuirn the related information in the format of either
JSON or XML.

##Sample Request to the API

http://dykapi.appspot.com/api/?format=json

http://dykapi.appspot.com/api/?format=xml

###Sample JSON output
	{"response": [
		{"hook": {
			"text": "The only known specimen of the extinct planthopper Glisachaemus jonasdamzeni 
					is preserved with a parasitic mite ", 
			"metadata": [
				{"metatext": "extinct", "metaurl": "http:\/\/en.wikipedia.org\/wiki\/Extinction"}, 
				{"metatext": "planthopper", "metaurl": "http:\/\/en.wikipedia.org\/wiki\/Planthopper"}, 
				{"metatext": "Glisachaemus jonasdamzeni", "metaurl": "http:\/\/en.wikipedia.org\/wiki\/Glisachaemus"}, 
				{"metatext": "mite", "metaurl": "http:\/\/en.wikipedia.org\/wiki\/Mite"}
				], 
			"title": "Glisachaemus"}
		}]
	}

###Sample XML output
	<response>
		<hook>
			<text>Addition of sulfur increases the refractive index of polymers </text>
			<metadata>
				<metatext>sulfur</metatext>
				<metaurl>http://en.wikipedia.org/wiki/Sulfur</metaurl>
			</metadata>
			<metadata>
				<metatext>refractive index of polymers</metatext>
				<metaurl>http://en.wikipedia.org/wiki/High_refractive_index_polymers</metaurl>
			</metadata>
			<title>High_refractive_index_polymers</title>
		</hook>
	</response>
