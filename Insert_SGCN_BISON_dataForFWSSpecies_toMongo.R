library(jsonlite)
library(tidyverse)
#library(mongolite)
library(rmongodb)


# Abby Benson - 20180227 - This script is meant to get the data that was pulled together in SGCNMatchedtoFWSNatWP.R and plug it
# in to the MongoDB FWS ESA Work Plan Species collection in the bis database. In the SGCNMatchedtoFWSNatWP.R script, I took a CSV
# with all of the scientific names and other data that FWS put together as the species they will be looking at for the next 7 
# years and matched those up to our SGCN data and BISON using scientific name. In this script I will take that SGCN and BISON data
# and add it back in to the FWS ESA Work Plan Species collection in MongoDB.

# First I need to grab the FWS ESA Work Plan Species collection from MongoDB
fwsListFromMongo <- mongo(collection = "xxxxxxxxxxxxxxxxxx", db = "xxxxxxxx", url = "xxxxxxx")
fwsMongo <- fwsListFromMongo$find('{}', fields = '{"_id":1, "Submitted Data":1}')
fwsMongo$`Scientific Name` <- fwsMongo$`Submitted Data`$`Scientific Name`
fwsMongo <- fwsMongo[c("_id", "Scientific Name")]

# Create SGCN dataframe that we would want to insert as a subdocument to the relevant document in MongoDB
sgcnInsertMongo <- sgcn_fwsListingWP[c("Scientific Name","Common Name", "Taxonomic Group", "Match Method", "statelist2015", "statelist2005")]
sgcnInsertMongo <- merge(sgcnInsertMongo, fwsMongo, by = "Scientific Name", all.x = T)
testSgcnInsertMongo <- sgcnInsertMongo[15,]
id <- testSgcnInsertMongo$`_id`
sgcnInsert <- as.list(testSgcnInsertMongo[,1:6])
sgcnInsert <- toJSON(sgcnInsert)

# Push SGCN data into MongoDB
sgcnInsertMongo$inserted <- NA
for (i in 1:nrow(sgcnInsertMongo)){
  if(is.na(sgcnInsertMongo[i,]$inserted)){
    id <- sgcnInsertMongo[i,]$`_id`
    sgcnInsert <- as.list(sgcnInsertMongo[i,1:6])
    sgcnInsert <- toJSON(sgcnInsert)
    fwsListFromMongo$update(query = paste0('{"_id": { "$oid" : "', id, '" } }'), update = paste0('{ "$set" : {"SGCN" :', sgcnInsert, '}}'))
    sgcnInsertMongo[i,]$inserted <- "done"
  }
}

# Push BISON data into MongoDB
bisonInsertMongo <- sgcn_fwsListingWP[c("Scientific Name", "bisonQuery", "bisontotal")]
bisonInsertMongo <- merge(bisonInsertMongo, fwsMongo, by = "Scientific Name", all.x = T)
bisonInsertMongo$inserted <- NA
for (i in 1:nrow(bisonInsertMongo)){
  if(is.na(bisonInsertMongo[i,]$inserted)){
    id <- bisonInsertMongo[i,]$`_id`
    bisonInsert <- as.list(bisonInsertMongo[i,2:3])
    bisonInsert <- toJSON(bisonInsert)
    fwsListFromMongo$update(query = paste0('{"_id": { "$oid" : "', id, '" } }'), update = paste0('{ "$set" : {"BISON" :', bisonInsert, '}}'))
    bisonInsertMongo[i,]$inserted <- "done"
  }
}
