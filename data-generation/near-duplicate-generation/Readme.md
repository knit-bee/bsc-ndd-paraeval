# near-duplicate-generation
To generate the datasets, it is necessary to first download the German word list that is used for the insertion of random words, e.g. with:
```sh
$ wget https://gist.githubusercontent.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4/raw/36b70dd6be330aa61cd4d4cdfda6234dcb0b8784/wordlist-german.txt

```
Then, (preferably after setting up a virtual environment,) install requirements with :
```sh
$ pip install -r requirements.txt
```

After that, the data generation can be conducted by calling the Python script and passing the name of the config file and the dataset that to process.
It is assumed that the German word list is located in the working directory and stored under the original name (`wordlist-german.txt`).

### Example:
Content of the config file :
```
[wikipedia]
input_dir=path/to/raw/data
output_dir=path/to/store/created/data
max_length=1821
average=411
```
Run the Python script with:
```sh
$ python near_dup_generation.py ndd-generation.cfg wikipedia
```
