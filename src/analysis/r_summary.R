
# load tidyverse package
library(tidyverse)

# load in csv file of scraped data
df <- read_csv("../../data/sneaker_info.csv")

#summarize
summary(df)
View(df)

# delete exact duplicates
df <- distinct(df)

