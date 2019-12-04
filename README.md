# PheGe Search
## Phenotype & Genotype Search
Search a massive ontological network for connections between phenotypes and genotypes.

Proper use of PheGe Search:
Required Parameters:
1. Sources file - csv file, first column is the gene ids second column is gene labels. Do not include any header lines or column names
2. Target file - csv file, first column is the gene ids second column is gene labels. Do not include any header lines or column names  
Optional Parameters
3. Type of plot output - options "webweb" or "default"
4. Output figure name - must a .png type. Figure will only be saved if using default type plot .   

### Example
```
python PheGe.py eeie-id-name.csv eeie-targets.csv default network-plot.png
```
