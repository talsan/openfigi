# openfigi
examples/notes using bloomberg's openfigi api to map tickers/company-names to bloomberg figis

### Use Cases
`mapping_tickers.py`: ticker + exchange --> bloomberg figis
`search_names.py`: search name + exchange --> bloomberg figis

### Working Notes:
1. Great for getting things into bloomberg ids, not out.
2. Unspecific requests yield unspecific responses. If inputs aren't listing specific (sedol/isin/cusip/ticker-exchange), expect many results for a given name/ticker (1->N).

### API Home
https://www.openfigi.com/api/

### Identifier Glossary
https://github.com/talsan/openfigi/blob/master/references/Open_Symbology_Fields-2a61f8aa4d.pdf

### More Resources
https://github.com/talsan/openfigi/tree/master/references
https://stockmarketmba.com/globalstockexchanges.php

### Related APIs
[Refinitive PermIds](https://developers.refinitiv.com/en/api-catalog/open-perm-id/permid-record-matching-restful-api)
