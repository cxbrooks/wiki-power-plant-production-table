# wiki-power-plant-production-table

Generate a Wikipedia table of electrical production data for a power plant.

# Purpose
Wikipedia has a number of pages for electrical power plants that have tables of production data from the U.S. Energy Information Administration (EIA).  It would be helpful if these tables could be automatically generated.

For example, [Ivanpah Solar Power Facility](https://en.wikipedia.org/wiki/Ivanpah_Solar_Power_Facility) has tables for each of the units and a summary table.  The table for Ivanpah 1 is based on [Electricy Data Browser](https://www.eia.gov/electricity/data/browser/#/plant/57074).

There are two sets of tables, one for "Net electricity production", the other for "natural gas consumption"

# Actions
* Given a power plant unit name, generate a wiki table of the data
* If a plant has multiple units, generate a summary table

# Nitty gritty
We need to be able to map from the Wikipedia page name to the the EIA page has "Plant name" and/or "Plant code".

# EAI API
The [EAI API](https://www.eia.gov/opendata/qb.php?category=0) requires that a user register for a key.

The net production data may be found at [EIA Data Sets > Electricity > Plant level data > California > (57073) Ivanpah 2 (57073)](https://www.eia.gov/opendata/qb.php?category=901385&sdid=ELEC.PLANT.GEN.57074-ALL-ALL.M)
