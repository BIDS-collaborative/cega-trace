library(XML)
a = htmlTreeParse(file.choose(),useInternal = TRUE)


ns <- getNodeSet(a, '//tr')

ns2=sapply(ns, xmlValue)

class(ns2)

#title
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

#citation
temp.cite=rep(0,length(ns2))
for (i in 1:length(ns2)){
  if (!is.null(ns2[i])){
    if (grepl("Z9 ", ns2[i])){
      temp.cite[i]=1
    }
  }
}
r=which(temp.cite %in% 1)
cite=ns2[r]
for (i in 1:length(cite)){
  t=cite[i]
  t=substr(t, 4, nchar(t))
  t=gsub('\n','',t)
  cite[i]=t
}
cite=as.integer(cite)
DATA=data.frame(DATA,'citation'=cite)

#Author
temp.au=rep(0,length(ns2))
for (i in 1:length(ns2)){
  if (!is.null(ns2[i])){
    if (grepl("AU ", ns2[i])){
      temp.au[i]=1
    }
  }
}
r=which(temp.au %in% 1)
au=ns2[r]
for (i in 1:length(au)){
  t=au[i]
  t=substr(t, 4, nchar(t))
  t=gsub('\n','',t)
  t=gsub('  ',';',t)
  au[i]=t
}
DATA=data.frame(DATA,'author'=au)
