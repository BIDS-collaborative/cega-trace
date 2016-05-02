
df <- data.frame()
for (i in 2:567){
  s <- paste0(i,"j.txt")
  a <- c()
  a[1] <-read.table(s)[1,1]
  a[2] <-read.table(s)[2,1]
  df <- rbind(df, a)
  print(i)
}
for (file in list.files(,"*j.txt")){
  if (file.size(file) == 0) next
  f <- read.table(file, sep = '\n', stringsAsFactors = FALSE)
  a <- data.frame(substr(file, 0, nchar(file) - 5), f[1,1], f[2,1])
  print(file)
  if (f[1,1]+f[2,1]!=0){
      df<- rbind(df, a)
  }
}

colnames(df) <- c("ID", "Journal", "Policy")

df$Percent <- df[,2]/(df[,2] + df[,3])
journel.percent <- df$Percent
hist(journel.percent, breaks = seq(0, 1, length.out = 40))
sum(df$Journal)
sum(df$Policy)
plot(df$Journal)

library(ggplot2)
ggplot(df1, aes(x = df1$X0L, y = df1$X9L)) + geom_point()



df_doi <- data.frame()

for (file in list.files(,"*doi.txt")){
  if (file.size(file) == 0) next
  f <- read.table(file, sep = '\n', stringsAsFactors = FALSE)
  for (j in 1:length(f[,1])) {
    a <- data.frame(substr(file, 0, nchar(file) - 7), f[j,1])
    print(j)
    if (f[j,1]!= "0"){
      df_doi<- rbind(df_doi, a)
      
    }
  }
}

colnames(df_doi) <- c("bookID", "doi")
df_doi$f.j..1.[which.max(table(df_doi$f.j..1.))]

plot(fdoi, xlab = "(df_doi)", type = 's', ylab = "Frequencies", label = fdoi)
freq <- table(df_doi$doi)
freq[1]
fdoi <- as.vector(freq)
sort(freq)[8899:8932]
max(fdoi)



f <- read.table(file, sep = '\n', stringsAsFactors = FALSE)
a <- c()
paste0(i,"doi.txt")
a <-read.table("2doi.txt", sep = '\n', stringsAsFactors = FALSE)
a[1,1]

a[2] <-read.table("2j.txt")[2,1]
df <- rbind(df, a)
