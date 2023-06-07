library(googledrive)

# Define a list of file IDs and corresponding output filenames
file_list <- list(
  "1qtmZVaws9_H6qGRjCVshXKG8YdZGrMZs" = "../../data/recent_purchases_2023-05-02.csv",
  "14d_FeeW7ZiPMEG2woItTRhtOyC0Hvzfz" = "../../data/recinfo_2023-05-02.csv",
  "12desa2-KUeRjGcVsutymeaG9YqLUtQxv" = "../../data/productlist20230501.csv",
  "1bWD7icRXeWf7Mvsrs3MzgjfvIFUaGoGF" = "../../data/productlist20230425.csv"
)

# Download each file and save it to the specified output filename
for (file_id in names(file_list)) {
  output_file <- file_list[[file_id]]
  drive_download(as_id(file_id), path = output_file)
}


