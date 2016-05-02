##load the data
load(file = "aid.rda")

##data cleaning(only keep the observation that has the first digit of sector code is 1, 2, or 3)
na = unique(c(which(is.na(aid$crs_purpose_code)), which(is.na(aid$commitment_amount_usd_constant)),
       which(is.na(aid$year))))
aid.na = aid[-na,]
aid.na$sec_3 = substr(aid.na$crs_purpose_code,start = 1 , stop = 3)
first = as.numeric(substr(aid.na$crs_purpose_code,start = 1 , stop = 1))
summary(first)
aid_ = aid.na[first == 1 | first == 2 | first == 3,]


##using data.table package
library(data.table)
DT  = data.table(aid_)
#sum up the value based on its year, recipient and the first three digits of sector code
DT = DT[,sum(commitment_amount_usd_constant), by = list(year,recipient,sec_3)]
#sort the DT
a = DT[order(sec_3),]
b = a[order(recipient),]
c = b[order(year),]
#sum up the value based on its year, recipient and the first digit of sector code
c$sec_1 = as.numeric(substr(c$sec_3,start = 1 , stop = 1))
d = c[,sum(V1), by = list(year,recipient,sec_1)]
