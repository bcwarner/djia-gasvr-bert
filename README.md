# csci330-project
This is Ben Warner and Aaron Crook's CSCI 330 F2019 term project. Here is an outline of the imporant scripts/files:

### `NYTData.py`
Running this script will repeatedly query the NYT API for the articles within a given date range specified within the file for the search terms specified within a CSV (ie `DJIACompCSV.csv`). Writes the results to a specified destination. On several instances, there were times we had to merge the files due to interruptions. The best output is `DJIAOutfComplete2.dat`

### `BERTModel.py`

There are several variations of this file, which was originally converted from the Jupyter notebook `MovieReviewsToHeadlines.ipynb`. This requires Tensorflow 1.15 and will process all of the headlines from `DJIAOutfComplete2.dat` and write the `Positive`/`Negative` classifications that BERT gives it to `datePredictions.pkl`

### `NYTDataProcessing.ipynb`

Used this to compile the headline statistics from `datePredictions.pkl`, which was then saved to `DJIAHeadlines.csv`


### `NYTBERTCombined.ipynb`

Used this to run the GA/SVR algorithm on the classification statistics, and then generate the plots.
