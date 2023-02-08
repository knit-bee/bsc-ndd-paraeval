# evaluation
First install requirements with (inside a virtual environment):
```sh
$ pip install -r requirements.txt
```
To run the deduplication experiments, first the gold standard has to be computed with:
```sh
$ python ground_truth_estimation.py dataset gold_dir
```
`dataset` is the path to the directory containing the data, `gold_dir` specifies the location where the files for the gold standard are stored.
(N.B.: Depending on the size of the dataset, this may take some time.)

After the computation of the gold standard is finished, the actual experiment can be conducted with the following command:
```sh
$ python run.py dataset config_dir gold_dir
```
Again, `dataset` is the directory where the data is stored, `gold_dir` the path to the gold standard. `config_dir` is the path to a directory where the parameter configurations are stored.
For examples on the format of the config file, see `../param_config`.
The experiment run will output a lot of files, so it is advisably to first create a new directory for the dataset that is processed and change the working directory to it:
```sh
$ mkdir dataset
$ cd dataset
```
Then, run the experiment by adjusting the paths accordingly.

For each parameter configuration, a matrix with the similarity scores for all files (stored as `scipy.sparse.csc_matrix` as `.npz`, split into multiple files) and a `numpy` array (in `.npy` format) with the NDCG-scores for each file are produced.
For each parameter configuration, the time needed for preprocessing and deduplication as well as the total average NDCG-score are logged.
