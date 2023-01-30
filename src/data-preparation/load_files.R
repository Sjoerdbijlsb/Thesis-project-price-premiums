# load tidyverse package
library(tidyverse)
library(stringr)
library(aws.signature)
library(aws.s3)
library(botor)
## Setting up the AWS S3 system

# Load the csv file containing the AWS access keys
aws_keys <- read.csv("../../../accesskeys_aws.csv", header = TRUE)
botor(region_name = 'us-east-1')

# Extract the access key ID and secret access key
aws_access_key_id <- as.character(aws_keys[1,1])
aws_secret_access_key <- as.character(aws_keys[1,2])

# Set up AWS credentials
Sys.setenv("AWS_ACCESS_KEY_ID" = aws_access_key_id,
           "AWS_SECRET_ACCESS_KEY" = aws_secret_access_key)


bucket <- "s3://pricepremiums/data/"
contents <- s3_ls(bucket)

# looping through the AWS s3 bucket to download all adjuststed files by "key" element
for (i in 1:nrow(contents)) {
  obj <- contents[i, "key"]
  last_modified <- as.Date(contents[i, "last_modified"], format = "%Y-%m-%d")
  today <- as.Date(Sys.Date())
  if (last_modified >= today - 7) {  # Only download files modified in the last 7 days
    save_object(obj, bucket, file = paste0("../../", obj), overwrite = TRUE)
  }
}
