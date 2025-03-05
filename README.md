<a className="gh-badge" href="https://datahub.io/core/co2-ppm-daily"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

This dataset was created using data from [Earth System Research Laboratory](https://www.esrl.noaa.gov/).
This data contains Atmospheric Carbon Dioxide Dry Air Mole Fractions from quasi-continuous daily measurements at Mauna Loa, Hawaii.


### Preparation

To generate output file you should only run the script:
`co2-ppm-daily-flow.py`

### Data

Data has been sourced from Scripps Laboratory, specifically: https://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/in_situ_co2/daily/daily_in_situ_co2_mlo.csv.

Output file is located in: `data/co2-ppm-daily.csv`

Value represents Mole fraction reported in units of micromol mol-1 (10-6 mol per mol of dry air); equivalent to ppm (parts per million).

## License

### ODC-PDDL-1.0

This Data Package is made available under the Public Domain Dedication and License v1.0 whose full text can be found at: http://www.opendatacommons.org/licenses/pddl/1.0/

### Notes

The [terms of use][gmd] of the source dataset list three specific restrictions on public use of these data:

> The information on government servers are in the public domain, unless specifically annotated otherwise, and may be used freely by the public so long as you do not 1) claim it is your own (e.g. by claiming copyright for NOAA information – see next paragraph), 2) use it in a manner that implies an endorsement or affiliation with NOAA, or 3) modify it in content and then present it as official government material.[*][gmd]

[ccgg-trends]: http://www.esrl.noaa.gov/gmd/ccgg/trends/index.html
[gmd]: http://www.esrl.noaa.gov/gmd/about/disclaimer.html
