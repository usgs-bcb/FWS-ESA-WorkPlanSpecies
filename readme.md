[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/usgs-bcb/FWS-ESA-WorkPlanSpecies/master)

# Provisional Software Disclaimer

Under USGS Software Release Policy, the software codes here are considered preliminary, not released officially, and posted to this repo for informal sharing among colleagues.

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.

# Introduction

This folder contains source data, processing codes (in the form of Jupyter Notebooks), a cache of processed data, and documentation for a data release of information associated with US Fish and Wildlife [National Listing Workplan](https://www.fws.gov/endangered/what-we-do/listing-workplan.html) species. This work is part of an overall response by USGS science centers and programs to characterize the current state of knowledge and expertise on these species that can be used to aid USFWS listing evaluation processes. The intent of this data release is to provide a tool for continuously updating a knowledge bank of available information that can be consulted at any time during the development and writing of Species Status Assessments or other aspects of the listing process.

## Setting up and running the code

The code in this repository is all Python based in Jupyter Notebooks. You can run the notebooks in Binder using the link at the top of the readme, or there is an environment.yml file or a requirements.txt file that can be used to set up a virtual environment in your platform of choice with the necessary dependencies. For instance, you can use Anaconda to set up a conda environment with the following once you clone the repository to your machine:

``conda create -f environment.yml``

The actual logic for the various processes run in the workflow folder come from an experimental Python package called [bispy](https://github.com/usgs-bcb/bispy) that is released as provisional software. This package and its dependencies are installed from source in the environment.yml or requirements.txt files. We welcome input on the processes run and the data produced. Due to the changing nature of the bispy experiment, we are maintaining branches of the code at particular checkpoints known to work with the various use cases we are running through. This is reflected in the environment files, or the major dependency for this work can be installed with the following:

``pip install git+git://github.com/usgs-bcb/bispy.git@v0.0.9``

Most of the processes for searching and assembling species information in the bispy package are from completely open and publicly accessible application programming interfaces (APIs) or web systems. The one exception is the IUCN Red List, which requires an IUCN API key to be established as an environment variable called "token_iucn." You can take advantage of the information we have already summarized from the IUCN Red List for this particular use in this package, but you will need to obtain your own IUCN Red List API token if you want to run that aspect of the data assembly process.

# Species and Capability Source Information

As a starting point for this work, we used a spreadsheet prepared internally to USGS that included a listing of the species taken from the original USFWS PDF file released online along with value-added information from a survey of USGS Science Centers and Cooperative Research Units seeking input on what previous and current research activities and capabilities might apply. A snapshot of this spreadsheet is included in the sources folder and is referenced in a number of the processing codes. An additional spreadsheet was prepared with a set of links for species to the USFWS Ecological Conservation Online System (ECOS) extracted from those embedded as Excel hyperlinks in one of the worksheets along with a set of explicit links to additional information sources for USGS Science Centers from the ScienceBase Directory.

# Contents

The work in this project is organized into several folders for convenience. Folder names correspond to the section descriptions describing their contents below.

## workflow

Some of the steps in this system build upon each other while others can be operated independently. The first couple of steps do build out the foundation for subsequent work and need to be run first.

1) Scrape and Cache ECOS data - This notebook describes and runs a process that uses a set of extracted links to ECOS Species pages to build a data structure with information for future work. The main thing this script does as setup is get the ITIS TSN identifier for species that was determined by FWS to be the correct ITIS taxonomy to use.

2) Transform and Cache Work Plan Info - This notebook starts up the master list for all additional work. It extracts the basic fields of information from the two source spreadsheets, stitches them together with the ITIS TSN pulled from the previous ECOS scraping step, and stashes a JSON document for further work.

3) Get additional FWS data from TESS - The final step to make sure we have all the best information to start further processing is to consult the FWS Threatened and Endangered Species System web service. We found that there were at least a couple of cases where, for whatever reason, the TESS service lookup for a given scientific name returns an ITIS TSN when the identifier was not found on the ECOS web page that we scraped previously. This step ensures that we have as many TSNs as possible to run taxonomic processing with ITIS. This step updates workplan_species with additional TSNs and caches a tess file for further consultation.

4) Consult with ITIS - The Integrated Taxonomic Information System is our initial best source for taxonomic data about the species. Most species in the FWS list have ITIS TSNs identified, and we use scientific names to search for the others. This script runs a parallel process to grab everything from the ITIS API and stash data in an itis.json file. The ITIS search function in the bispy package can be operated in a number of different ways, but here we grab both valid/accepted and invalid/unaccepted taxonomic records but then follow ITIS to valid/accepted taxonomy, storing all relevant documents.

5) Consult with WoRMS - An additional taxonomic authority we use for marine and some estuarine species is the World Register of Marine Species. We found here that there were a number of mollusc species in WoRMS that are not currently found in ITIS. Because we are essentially treating ITIS as primary authority (since that is the decision made by FWS), we only run names that we could not find in ITIS through the WoRMS lookup process. The resulting 24 additional taxonomic identifications were stashed in a worms.json file.

6) Finalize Workplan Species List - Before we move on to other information assembly steps, it is useful to explore anything we might have discovered with taxonomic authorities that may lend new or improved information for species lookup. This notebook examines cases where the original information from the workplan species list resulted in something other than an exact match in ITIS from either a declared ITIS TSN or scientific name lookup. It rebuilds the workplan species source with additional information from ITIS that can be used in searches. A quick look at the WoRMS results showed that we only returned exact matches for the handful of species that we did not find in ITIS but were able to find in WoRMS, so there is essentially no additional information from the standpoint of species lookups that we need to assemble from that source at this time.

7) The following information gathering functions can all be run once the workplan_species.json dataset has been built from source data and additional names from ITIS. The local helperfunctions.py file was added with a simple function to read the workplan_species data and build a list of name/name source tuples for use throughout the information gatherers.
* Check SGCN List - Checks to see what species have also been identified on State Species of Greatest Conservation Need lists; notably provides state names that can be compared with states identified in the range information for work plan species
* Check IUCN Species - Checks to see what species have been assessed in the IUCN process; notably provides global perspective in conservation status and links to published assessment reports on habitats, threats, and needed conservation measures
* Check NatureServe Species - Checks to see what species have been included in the NatureServe species data system; notably provides information on national conservation status, additional taxonomic information, and links to further assessment details
* Check GAP Species and GAP Suggested Range - Establishes links to the terrestrial vertebrate species managed through the USGS Gap Analysis Project; notably includes a suite of information on species habitat requirements, range and habitat maps, and a summarization process that indicates protection status within states where habitat classes have been mapped
* Check xDD Library - Searches a library of scientific papers and reports for species names; provides snippets of text form papers and access information
* Summarize GBIF Species - Searches GBIF for a species and uses suggested taxa to summarize occurrence data; notably includes a couple of facet reports that indicate the type of occurrence records in GBIF and where they come from
* Check ScienceBase Data Release Products - Searches ScienceBase for official Data Release Products associated with the species names to summarize available data products that may be of interest

## reports

To help make the data easier to digest, we provide a couple of report options, one that explores some dynamics with the taxonomy and one that summarizes high level properties into a simplified CSV file.

1) Summarize Properties to CSV - This notebook makes a number of choices about how to "flatten" the data structures into a simpler set of high level properties that can be opened in a spreadsheet program and examined in various ways. The results are output to the cache folder.

2) Examine Taxonomy - This notebook works through all of the cases where our process was unable to find valid or accepted records in ITIS by either following the Taxonomic Serial Number found from the Ecological Conservation Online System records or by searching the scientific name in the FWS Work Plan.

## cache

Data outputs from the workflow steps are cached as JSON or CSV files and stored in the cache folder. These are point in time snapshots of the data assembled for the FWS Work Plan species with embedded datetime stamps indicating when the records were produced.

## documentation

The documentation folder contains JSON Schema documents for each JSON data file in the data cache that documents the structure and properties of the data built through the processing workflow. The schemas are exercised at the end of each workflow to validate the data produced. These documents stand in place of more traditional entity and attribute information in the FGDC CSDGM standard or ISO Feature Catalog. There is also an ISO19115 metadata XML document at the root of the project that describes the whole data release product.

# Data Management Plan and Considerations

As a fully contained workflow system, this data package has information associated with data management documented throughout. Notebooks in the workflow contain applicable data management considerations documented as part of the notes where users will need to consider particular implications for future update and development of the information.

Perhaps the most important overarching data management dynamic to consider is one of timeliness and necessary updates. As a data assembly workflow, pulling information from across the web, this package is almost immediately potentially stale and out of date. This is why we refer to the data as a cache; because it is retrieved, transformed, and cached information from various sources. Each record in the cached datasets contains a processing_metadata object with a standard set of information on when the record was produced, what API was used, and how the process went when it ran. Additionally, some records will have a separate parameters object containing some variable key/value pairs when needed to describe the input parameters that went into producing the record. This information can be used to evaluate when a particular process should be run again to refresh data.

One of the more crucial potential updates, in some ways, is the connection of the source species list to taxonomic authorities. As biological taxonomy progresses through time, new information is added to sources like ITIS and WoRMS used here that may alter thinking about the source list and will likely impact how information is linked to and retrieved from online sources. We've also not yet accounted for some overarching function to examine or account for this dynamic in a system like this one.
