To download specific codes limiting the max. of pictures downloaded:

```
python3 bird_crawler.py --data_path /my/data/path/ --codes 1 6 7 --limit 3000 

```

By default it skips species with an existing picture folder in data_path/pictures. To force download:

```
python3 bird_crawler.py --data_path /my/data/path/ --codes 1 6 7 --limit 3000 --overwrite

```

To download a random sample size N of species that haven't been downloaded:

```
python3 bird_crawler.py --data_path /my/data/path/ --random_codes N --limit 20

```