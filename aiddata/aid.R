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
####  V1 here stands for commitment_amount_usd_constant




###IDA and IBRD
load(file = "aidDB.full.rda")


###levels(aidfull$donor)[111],[112]
aid2.ibrd = aidfull[aidfull$donor == levels(aidfull$donor)[111], c(2,17,15,28)]
aid2.ida = aidfull[aidfull$donor == levels(aidfull$donor)[112], c(2,17,15,28)]

DT  = data.table(aid2.ibrd)
ibrd = DT[,sum(commitment_amount_usd_constant), by = list(year)]
ibrd = ibrd[order(year),][15:65,]
colnames(ibrd) = c("year", "commitment_amount_usd_constant")

DT  = data.table(aid2.ida)
ida = DT[,sum(commitment_amount_usd_constant), by = list(year)]
ida = ida[order(year),]
colnames(ida) = c("year", "commitment_amount_usd_constant")

##CPIA
#cpia = read.csv("CPIA score average.csv", header = T, strip.white = T)[,c(1:3,9:13)]
#DT = data.table(cpia)
#cpia. = DT[,list(sum(econ.1),sum(social.1), sum(public.1), sum(structure.1), 
#                sum(policy.1)), by = list(year)][16:24]




cpia = read.csv("CPIA score average.csv", header = T, strip.white = T)

join.ida = merge(x = cpia, y = ida, by = "year", all.x = TRUE)
join = join.ida[order(join.ida$id),]

join.ibrd = merge(x = join, y = ibrd, by = "year", all.x = TRUE)
join = join.ibrd[order(join.ibrd$id),]
colnames(join)[14:15] = c("ida", "ibrd")

##Add Class and Growth Rate to "join" 
library(xlsx)
library(reshape2)
gdp = read.xlsx("GDP per capita growth rate.xlsx", sheetIndex = 1)[-c(215,216),-c(1:3)]
colnames(gdp)[-1] = 1990:2013

melt.gdp = melt(gdp, id.vars = c("Country.Code"))
colnames(melt.gdp) = c("code", "year", "gdp")
join.gdp = merge(x = join, y = melt.gdp, by = c("code", "year"), all.x = TRUE) 





class = read.xlsx("historical country classification.xlsx", sheetIndex = 2)[-c(1:9),-2]
colnames(class) = c("code", 1990:2013)

melt.class = melt(class, id.vars = "code")
colnames(melt.class) = c("code", "year", "class")
join.class = merge(x = join.gdp, y = melt.class, by = c("code", "year"), all.x = T)

