# Web scraping bird pictures and audio

This repository contains code use to scrape image and audio recordings of birds. This is not meant to be used as a general purpose scraper.

## Requirements:


## Usage:

There are two necessary inputs:
- A URL for the reference sheet listing all species.
- A base request URL to download media for species.

### Download reference sheet

```
python download_ref_sheet.py path/to/data/dir
```

### Download audio

### Download pictures


## Docker usage:

First, to build the container from Dockerfile run:

```
docker build -t crawler .
```

To download specific codes limiting the max. of pictures downloaded:

```
 docker run --volume=/my/data/path/:/pokedex --rm -ti crawler --codes 1 6 7 --limit 3000 

```

By default it skips species with an existing picture folder in data_path/pictures. To force download:

```
 docker run --volume=/my/data/path/:/pokedex --rm -ti crawler --codes 1 6 7 --limit 3000 --overwrite

```

To download a random sample size N of species that haven't been downloaded:

```
 docker run --volume=/my/data/path/:/pokedex --rm -ti crawler --random_codes N --limit 20

```
