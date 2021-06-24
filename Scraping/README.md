First, build the container from Dockerfile:

```
docker build -t crawler .
```

To download specific codes limiting the max. of pictures downloaded:

```
 docker run --volume=/my/data/path/:/pokedex crawler --codes 1 6 7 --limit 3000 

```

By default it skips species with an existing picture folder in data_path/pictures. To force download:

```
 docker run --volume=/my/data/path/:/pokedex crawler --codes 1 6 7 --limit 3000 --overwrite

```

To download a random sample size N of species that haven't been downloaded:

```
 docker run --volume=/my/data/path/:/pokedex crawler --random_codes N --limit 20

```