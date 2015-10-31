library(XML)
a = htmlTreeParse(file.choose(),useInternal = TRUE)


ns <- getNodeSet(a, '//tr')

ns2=sapply(ns, xmlValue)

class(ns2)

temp_title=rep(0,length(ns2))

for (i in 1:length(ns2)){
  if (!is.null(ns2[i])){
    if (grepl("TI ", ns2[i])){
      temp_title[i]=1
    }
  }
  
}

r=which(temp_title %in% 1)
title=ns2[r]
title
for (i in 1:length(title)){
  t=title[i]
  t=substr(t, 4, nchar(t))
  t=gsub('\n','',t)
  
  title[i]=t
}
DATA=data.frame('title'=title)
