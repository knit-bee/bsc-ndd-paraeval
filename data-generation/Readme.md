## Data generation
This directory contains the Python scripts with which the datasets were created.
The processing was conducted as follows:
- Download raw data
- Clean data, if necessary
- Split into paragraphs
- (Compute average paragraph length to exclude outliers)
- Generate near-duplicates


For the generation of the near-duplicates, the [*augtxt*](https://github.com/ulf1/augtxt) package as well as a list of German words (downloadable from [here](https://gist.githubusercontent.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4/raw/36b70dd6be330aa61cd4d4cdfda6234dcb0b8784/wordlist-german.txt)) was used.

The 'ndd-generation.cfg' file contains the configuration for the near-duplicate generation. It stores the average and maximum character count of a document for each dataset that were computed using *wc*.
