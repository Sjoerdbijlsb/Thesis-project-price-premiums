# Online Boutique stores: what what factors drive product recommendations in limited-edition resale markets?

This Repository accompanies my thesis that investigates product recommendations in the thriving fashion resale market. The platform uses product recommendations and recent 
product purchases from [GOAT](https://www.goat.com/), one of the biggest resale platforms in this industry.

# Repository overview
The set up of the files in this project are as follows:
```
├── data
└──  gen
   ├── output
└── src
   ├── analysis
   ├── data-collection
   ├── data-preparation
├── paper
├── .gitignore
├── README.md
├── makefile

```

# Data [(direct link to data)](https://drive.google.com/drive/u/0/folders/1HfVG22n4h4il92tmDk6Abf5qtocoBxyZ)


## Dataset desription

```
(1) recinfo_2023-05-02.csv
-Product recommendations(rec_id) per size and product condition (new, used, etc.)
-Relevant product info on brand, release date, color etc.
-The variable display_order refers to the ranking in one of the recommendation lists (each have up to 8 per product).
-For variables that have a display_order of 0, the product info refers to the product that was sampled and where the recommendations are shown(id).

(2) recent_purchases_2023-05-02.csv
-Recent purchases with timestamp for all recommendations in file 1.
-Location of sale included.

(3) productlist20230501.csv
-The top 10,000 products from GOAT's search [list](https://www.goat.com/search) for apparel and sneaker categories, with some product information such as retail price, last sold price.
-Product info here is not based on size per product.

(4) productlist20230425.csv
-Similar to file 3, with a wider selection outside the top 20,000 (100,000 + products)


* Note: file 3 and 4 are first used to draw a sample from in this analysis. File 1 and 2 are used directly in preparing the data and the analysis.
```


# Run study with the same data
The analysis can also be replicated by running the . This can be done easily if you have installed [make](https://gnuwin32.sourceforge.net/packages/make.htm).


## Check dependencies first


# Gather new data
In case you want to gather the data from scratch, you can make use of the scrapers in this file.


# Contact
s.bijl_1@tilburguniversity.edu
