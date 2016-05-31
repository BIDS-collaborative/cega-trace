# load filtered data

library(readr)
mpij_rep_poor <- read_csv("mpij_rep_poor.csv")

# Change the column names of "d"
colnames(d) <- c("year", "country", "sec_1", "usd_constant")

d$year <- as.numeric(d$year)
d$country <- as.character(d$country)


# Make a new column that shows the proportion of sector 1 to sector 2
x <- NULL
for (i in 1:length(d$usd_constant)) {
  y <- d$usd_constant[d$year == d$year[i] & d$country == d$country[i] & d$sec_1 == 1]
  z <- d$usd_constant[d$year == d$year[i] & d$country == d$country[i] & d$sec_1 == 2]
  if (isTRUE(as.logical(y)) & isTRUE(as.logical(z))) {
    x[i] <- y/z
  } else {
    x[i] <- "NA"
  }
}

# Attach this data to the original data frame

d$"sec1/sec2" <- as.numeric(x)

# Make a new column that shows the proportion of sector 1 to sector 3
x1 <- NULL
for (i in 1:length(d$usd_constant)) {
  y <- d$usd_constant[d$year == d$year[i] & d$country == d$country[i] & d$sec_1 == 1]
  z <- d$usd_constant[d$year == d$year[i] & d$country == d$country[i] & d$sec_1 == 3]
  if (isTRUE(as.logical(y)) & isTRUE(as.logical(z))) {
    x1[i] <- y/z
  } else {
    x1[i] <- "NA"
  }
}

# Attach this data to the original data frame

d$"sec1/sec3" <- as.numeric(x1)


# Make a new column that shows the proportion of sector 1 to sector 2 & sector 3
x2 <- NULL
for (i in 1:length(d$usd_constant)) {
  y <- d$usd_constant[d$year == d$year[i] & d$country == d$country[i] & d$sec_1 == 1]
  z <- d$usd_constant[d$year == d$year[i] & d$country == d$country[i] & d$sec_1 == 2] + 
    d$usd_constant[d$year == d$year[i] & d$country == d$country[i] & d$sec_1 == 3]
  if (isTRUE(as.logical(y)) & isTRUE(as.logical(z))) {
    x2[i] <- y/z
  } else {
    x2[i] <- "NA"
  }
}

# Attach this data to the data frame
d$"sec1/(sec2+sec3)" <- as.numeric(x2)


# Substitute the columns that we need
d_new <- as.data.frame(d)[,c("year", "country", "sec1/sec2", "sec1/sec3","sec1/(sec2+sec3)")]

d_final <- unique(d_new)


# Now we can merge two data frames
library(plyr)
merged1 <- ddply(merge(mpij_rep_poor, d_final, all.x=TRUE), .(year, country))

merged2 <- ddply(merge(d_final, mpij_rep_poor, all.x=TRUE), .(year, country))


# Work with residual values and create new column named "resid_cat"
resid_cat <- NULL
for (i in 1:length(merged1$country)) {
  if (merged1$residv[i] >= 1) {
    resid_cat[i] <- "ipoor"
  } else if (merged1$residv[i] <= -1) {
    resid_cat[i] <- "cpoor"
  } else {
    resid_cat[i] <- "poor"
  }
}

merged1$"resid_cat" <- resid_cat

# Work with residual values and created new column named "resid_med_cat"
resid_med_cat <- NULL
for (i in 1:length(merged1$country)) {
  med <- median(merged1$residv)
  dif <- med - merged1$residv[i]
  if (dif > 0.99) {
    resid_med_cat[i] <- "cpoor"
  } else if (dif < -0.99) {
    resid_med_cat[i] <- "ipoor"
  } else {
    resid_med_cat[i] <- "poor"
  }
}

merged1$"resid_med_cat" <- resid_med_cat

# Changing "resid_med" column
for (i in 1:length(merged1$resid_med)) {
  if (merged1$resid_med[i] == 1) {
    merged1$resid_med[i] <- "ipoor"
  } else {
    merged1$resid_med[i] <- "cpoor"
  }
}


# Re-order the columns
merged_final <- merged1[, c(1:4, 87:89, 5,6,7,8,90,9,91,10:86)]
write.csv(merged_final, "merged_new.csv")
