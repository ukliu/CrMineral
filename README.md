# CrMin
A template for building applications to extract information from published documents in the [GeoDeepDive](https://geodeepdive.org) infrastructure

## Getting started
Dependencies:
  + [GNU Make](https://www.gnu.org/software/make/)
  + [git](https://git-scm.com/)
  + [pip](https://pypi.python.org/pypi/pip)
  + [PostgreSQL](http://www.postgresql.org/)

### OS X
OS X ships with GNU Make, `git`, and Python, but you will need to install `pip` and PostgreSQL. OS X is not a requirement, but development on a \*nix distribution is assumed here.

To install `pip`:
````
sudo easy_install pip
````

To install PostgreSQL, it is recommended that you use [Postgres.app](http://postgresapp.com/). Download
the most recent version, and be sure to follow [the instructions](http://postgresapp.com/documentation/cli-tools.html)
for setting up the command line tools, primarily adding the following line to your `~/.bash_profile`:

````
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin
````


### Setting up the project
First, clone this repository and run the setup script:

````
git clone https://github.com/UW-DeepDive-Infrastructure/app-template
cd app-template
make
````

Edit `credentials` with the connection credentials for your local Postgres database.

To create a database with the data included in `./input`:

````
make local_setup
````

To run an example application and check its output:

```
python run.py
cat output/proper_nouns_with_adjectives
```

## Inputs
The `./input` directory contains an example of the possible inputs. These include:

  * Cuneiform OCR output (cuneiform-page-000\*.html)
  * Tesseract OCR output (page-\*.hocr.html)
  * TSV dumps of sentence-level NLP processings with varying Stanford CoreNLP version and output formatting
  * bibjson file containing the article's bibliographic information.

 See `./input/README` for more details on each product.

Applications should be written with the expectation that full data products
matching the desired terms will be available within the `./input`.


## Running on GeoDeepDive Infrastructure
All applications are required to have the same structure as this repository, namely an empty folder named `output`, a valid
`config` file, an updated `requirements.txt` describing any Python dependencies, and `run.py` which runs the application
and outputs results. The `credentials` file will be ignored and substituted with a unique version at run time. The `input`
directory will similarly be substituted with the complete set of desired products matching the terms (or dictionary) specified.

The GeoDeepDive infrastructure will have the following software available:
  + Python 2.7+ (Python 3.x not supported at this time)
  + PostgreSQL 9.4+, including command line tools and PostGIS

#### Submitting a config file
The `config` file outlines a list of terms OR dictionaries that you are interested in culling from the corpus. Once you have
updated this file, a private repository will be set up for you under the UW-DeepDiveInfrastructure Github group for you to
push the code from this repository to. Your `config` file will be used to generate a custom testing subset of documents that
you can use to develop your application.

#### Running the application
Once you have developed your application and tested it against the corpus subset, simply push your application to the
private repository created in the previous step. The application will then be run according to the parameters set in the
`config` file.

#### Getting results
After the application is run, the contents of the `output` folder will be gzipped and be made available to download. If
an error was encountered or your application did not run successfully any errors thrown will be logged into the file
`errors.txt` which is included in the gzipped results package.

## File Summary

#### config
A YAML file that contains project settings.


#### credentials
A YAML file that contains local postgres credentials for testing and generating examples.


#### requirements.txt
List of Python dependencies to be installed by `pip`


#### run.py
Python script that runs the entire application, including any setup tasks and exporting of results to the folder `./output`.


## License
CC-BY 4.0 International
