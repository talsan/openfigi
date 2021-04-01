# openfigi
Examples, notes, and refereces for using Bloomberg's OpenFIGI api to map tickers/company-names to bloomberg figis

### Examples Contained Here
1. `mapping_tickers.py` ticker + exchange --> bloomberg figi
2. `search_names.py` search name + exchange --> bloomberg figi

### Working Notes:
1. Great for getting things into bloomberg ids, not out.
2. Unspecific requests yield unspecific responses. If inputs aren't listing specific (sedol/isin/cusip/ticker-exchange), expect many results for a given name/ticker (1->N).

### API Home
https://www.openfigi.com/api/

### Structure
![figi_tree](https://github.com/talsan/openfigi/blob/master/references/figi_tree.jpg?raw=true)

### Identifier Glossary

Code|Name|Description
----|----|-----------
`NAME`|Name|Name of the company or brief description of the instrument. The Name of an instrument may change in conjunction with corporate actions.
`TICKER`|Ticker|Ticker is a specific identifier for a financial instrument that reflects common usage. Tickers are not, however, unique to specific exchanges or specific pricing sources. Tickers may change in conjunction with Corporate Actions.
`EXCH_CODE`|Exchange Code| Code for the trading venue or environment on which the instrument trades. If an exchange is specified, the code will be for the specified exchange. When not specified, the code will be according to the user default exchange, which can be the composite or primary exchange.
`SECURITY_TYP`|Security Type|Description of the specific instrument type within its market sector.
`ID_BB_SEC_NUM_DES`|Security ID Number Description| Descriptor for a financial instrument. Equities: Not unique on the exchange level; must be combined with Feed Source (DX282, FEED_SOURCE) to achieve a unique value at the exchange level.
`MARKET_SECTOR_DESCRIPTION`|Market Sector Description|Market Sector refers to the asset type assigned to the instrument.
`ID_BB_GLOBAL`|Financial Instrument Global Identifier| Twelve character, alphanumeric identifier. The first 2 characters are upper-caseconsonants (including "Y"), the third character is the upper-case "G", characters 4 -11 are any upper-case consonant (including "Y") or integer between 0 and 9, and the last character is a check-digit. An identifier is assigned to instruments of all asset classes, is unique to an individual instrument and once issued will not change for an instrument. **For equity instruments an identifier is issued per instrument per trading venue.**
`COMPOSITE_ID_BB_GLOBAL`|Composite Financial Instrument Global Identifier| Twelve character, alphanumeric identifier. The first 2 characters are upper-case consonants (including "Y"), the third character is the upper-case "G", characters 4 -11 are any upper-case consonant (including "Y") or integer between 0 and 9, and the last character is a check-digit. The Composite level of assignment is provided in cases wherethere are multiple trading venues for the instrument within a single country or market. **The Composite Financial Instrument Global Identifier (FIGI) enables users to link multiple FIGIs at the trading venue-level within the same country or market in order to obtain an aggregated view for that instrument within that country or market.**
`ID_BB_GLOBAL_SHARE_CLASS_LEVEL`|Share Class Financial Instrument Global Identifier| Twelve character, alpha-numeric identifier. The first 2 characters are upper-case consonants (including "Y"), the third character is the upper-case "G", characters 4 -11 are any upper-case consonant (including "Y") or integer between 0 and 9, and the last character is a check-digit. **A Share Class level Financial Instrument Global Identifier is assigned to an instrument that is traded in more than one country. This enables users to link multiple Composite FIGIs for the same instrument in order to obtain an aggregated view for that instrument across all countries globally.**
`ID_BB_UNIQUE`|Unique Identifier|A legacy identifier assigned to all instruments. The construction and length of thisidentifier is different across asset classes. This identifier can also change as a result of corporate actions.
`SECURITY_TYP2`|Security Type 2|A description of the security type.
`SECURITY_DESS`|Security Description|A description of the security
`UNIQUE_ID_FUT_OPT`|Unique Identifier for Future Option|Unique ticker with logic for index, currency, single stock futures, commodities andcommodity options. This identifier differs from the Unique Identifier in that it is a logical ticker.
`MARKET_SECTOR`|Market Sector Number|Number of the market sector of the security. Possible returns are: 1. Commodity; 2. Equity; 3. Municipals; 4. Preferred; 6. Money Market; 7. Government; 8. Corporate; 9. Index; 10. Currency; 11. Mortgage;
`SECURITY_SHORT_DES`|Security Short Description| Alternate Short Description for a given security comprised of the ticker, coupon and maturity year (YY). For strips it returns the ticker, coupon, and maturity (M/YY). For corporate securities with Japanese tickers, the series will also be displayed.

https://github.com/talsan/openfigi/blob/master/references/Open_Symbology_Fields-2a61f8aa4d.pdf


### More Resources
* https://github.com/talsan/openfigi/tree/master/references
* https://stockmarketmba.com/globalstockexchanges.php

### Related APIs
[Refinitive PermIds](https://developers.refinitiv.com/en/api-catalog/open-perm-id/permid-record-matching-restful-api)
