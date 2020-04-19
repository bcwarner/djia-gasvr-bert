# Predicting the DJIA with news headlines and historic data using hybrid genetic algorithm/support vector regression and BERT
This is the repository for our model that was submitted to the BigData 2020 conference. Here is an outline of the imporant scripts/files:

### `NYTData.py`
Running this script will repeatedly query the NYT API for the articles within a given date range specified within the file for the search terms specified within a CSV (ie `DJIACompCSV.csv`). Writes the results to a specified destination. On several instances, there were times we had to merge the files due to interruptions. The best output is `DJIAOutfComplete2.dat`

### `BERTModel.py`

There are several variations of this file, which was originally converted from the Jupyter notebook `MovieReviewsToHeadlines.ipynb`. This requires Tensorflow 1.15 and will process all of the headlines from `DJIAOutfComplete2.dat` and write the `Positive`/`Negative` classifications that BERT gives it to `datePredictions.pkl`

### `NYTDataProcessing.ipynb`

Used this to compile the headline statistics from `datePredictions.pkl`, which was then saved to `DJIAHeadlines.csv`. We later applied a filter to the data, which can be found in this notebook.


### `NYTBERTCombined.ipynb`

Used this to run the GA/SVR algorithm on the classification statistics, and then generate the plots.
