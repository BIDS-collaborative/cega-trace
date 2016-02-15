# import libraries
library(data.table)
library(ggplot2)
library(rworldmap)

# set working directory and read csv files
setwd("/Users/manjiangjie/Desktop/Coding/")
aiddata <- fread("aiddata2-1_research release.csv")
DT <- as.data.table(aiddata)

# filter out "cash transfer" related rows
DT_CT1 <- DT[grepl(c("CASH TRANSFER"), short_description)]
DT_CT2 <- DT[grepl(c("ash Transfer"), long_description)]
DT_CT3 <- DT[grepl(c("ash transfer"), long_description)]
DT_CT4 <- DT[grepl(c("CASH TRANSFER"), long_description)]
DT_CT5 <- DT[grepl(c("ash Transfer"), title)]
DT_CT6 <- DT[grepl(c("ash transfer"), title)]
DT_CT7 <- DT[grepl(c("CASH TRANSFER"), title)]

# append all rows together and sort by years
l <- list(DT_CT1, DT_CT2, DT_CT3, DT_CT4, DT_CT5, DT_CT6, DT_CT7)
DT_CT <- rbindlist(l, use.names=TRUE)
DT_CT <- DT_CT[order(year)]
View(DT_CT)

# write to join_table.csv
setwd("/Users/manjiangjie/Desktop/Coding/Projects/cega-trace/data")
write.csv(DT_CT, file = "aiddata_cash_transfer.csv")



# # group by year and recipient
# aiddata_clean <- DT[, .(sum(disbursement_amount_usd_constant), sum(commitment_amount_usd_constant)), by = .(year, recipient_iso3)]
# setnames(aiddata_clean, "V1", "disbursement")
# setnames(aiddata_clean, "V2", "commitment")
# setkey(aiddata_clean, year)
#
# # same with research.csv and join them together
# setwd("/Users/manjiangjie/Desktop/Coding/Projects/cega-trace/data")
# research <- fread("research.csv")
# 
# DT <- as.data.table(research)
# setkey(DT, Year)
# research_clean <- DT[, .(Year, Title, Author, Journal)]
# join_table1 <- aiddata_clean[research_clean, allow.cartesian=TRUE]
# 
# # same with policy.csv and join them together
# policy <- fread("policy.csv")
# DT <- as.data.table(policy)
# setkey(DT, Report_publication_yr)
# policy_clean <- DT[, .(Report_publication_yr, Title, Author)]
# join_table2 <- join_table1[policy_clean, allow.cartesian=TRUE, nomatch = NA]
# 
# new_join_table <- na.omit(join_table2)
# 
# # some plots
# plot(density(new_join_table$year, na.rm = TRUE), main = "Year distribution")
# p <- ggplot(new_join_table, aes(x = year, y = disbursement, colour = factor(recipient_iso3)))
# p + geom_point() + geom_smooth()
# 
# # world map plot
# sPDF <- joinCountryData2Map(new_join_table, joinCode = "ISO3", nameJoinColumn = "recipient_iso3")
# par(mai=c(0,0,0.2,0),xaxs="i",yaxs="i")
# mapDevice()
# mapCountryData(sPDF, nameColumnToPlot = "Journal")
# mapCountryData(sPDF, nameColumnToPlot = "disbursement")
# mapCountryData(sPDF, nameColumnToPlot = "commitment")
# mapCountryData(sPDF, nameColumnToPlot = "year", catMethod = c(1999:2011))
