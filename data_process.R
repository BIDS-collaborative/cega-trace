library(data.table)
library(ggplot2)
library(rworldmap)

# set working directory and read csv files
setwd("/Users/manjiangjie/Desktop/")
aiddata <- fread("aiddata2-1_research release.csv")
DT <- as.data.table(aiddata)

# group by year and recipient
aiddata_clean <- DT[, .(sum(disbursement_amount_usd_constant), sum(commitment_amount_usd_constant)), by = .(year, recipient)]
setnames(aiddata_clean, "V1", "disbursement")
setnames(aiddata_clean, "V2", "commitment")
setkey(aiddata_clean, year)

# same with research.csv and join them together
setwd("/Users/manjiangjie/Desktop/Coding/Projects/cega-trace/data")
research <- fread("research.csv")

DT <- as.data.table(research)
setkey(DT, Year)
research_clean <- DT[, .(Year, Title, Author, Journal)]
join_table1 <- aiddata_clean[research_clean, allow.cartesian=TRUE]

# same with policy.csv and join them together
policy <- fread("policy.csv")
DT <- as.data.table(policy)
setkey(DT, Report_publication_yr)
policy_clean <- DT[, .(Report_publication_yr, Title, Author)]
join_table2 <- join_table1[policy_clean, allow.cartesian=TRUE, nomatch = NA]

new_join_table <- na.omit(join_table2)

# some plots
plot(density(new_join_table$year, na.rm = TRUE), main = "Year distribution")
p <- ggplot(new_join_table, aes(x = year, y = disbursement, colour = factor(recipient)))
p + geom_point() + geom_smooth()

# world map plot
sPDF <- joinCountryData2Map(new_join_table, joinCode = "NAME", nameJoinColumn = "recipient")
par(mai=c(0,0,0.2,0),xaxs="i",yaxs="i")
mapDevice()
mapCountryData(sPDF, nameColumnToPlot = "Journal")
mapCountryData(sPDF, nameColumnToPlot = "disbursement")
mapCountryData(sPDF, nameColumnToPlot = "commitment")
mapCountryData(sPDF, nameColumnToPlot = "year", catMethod = c(1999:2011))

# write to join_table.csv
setwd("/Users/manjiangjie/Desktop/")
write.csv(new_join_table, file = "join_table.csv")
