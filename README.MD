# DASH-HLS-GENERATOR

This project offers a simple config-file based approach to prepare streaming media. It greatly simplifies the process of
using FFmpeg for both VOD and live content.

## TODO:
- [ ] Document passed config 
- [ ] Set up the representations shuffle process 
- [ ] Add option to delete local generated file
- [ ] Connect to mongo database to save the metadata and url 
## Installation & Usage

### Pre-Requisites

- [Anaconda](https://www.anaconda.com/) is installed
- [FFMPEG](https://ffmpeg.org/) is installed 
- An environment with Python 3.7 or greater installed 
### Setup

##### 1. Clone the project and install all needed dependencies.

```bash
# Clone the project
git clone git@github.com:Mcamin/DASH-HLS-Generator.git
# 
# Create environment and  install dependencies
conda env create --name dash --file environment.yml 
```

##### 2. Setup Environment Variables

For a quick start, copy the default environment file.

```
cp .env.default .env
```

Afterwards, your `.env` file should look like this:

```
AWS_ACCESS_KEY_ID="THE ACCESS KEY ID"
AWS_SECRET_ACCESS_KEY="The SECRET ACCESS KEY"
BUCKET_NAME="BUCKET"
FFMPEG="FFMPEG PATH"
```

you can set the environment variables according to your local setup.

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are the amazon needed credentials to access the bucket.
    If not passed the files will be kept locally given output folder in the configs
- `BUCKET_NAME` is the name of the bucket setup on amazon to be used for storing and delivering content.
- `FFMPEG` is the path to the ffmpeg binary.




### Config Documentation
To be added

### Docker 
To be added 

### Things to consider

- This project follows the GitFlow Workflow, with features and release branches. Learn more
  here: [GitFlow Tutorial](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- Merges to the `master` branch automatically trigger a deployment to the staging environment, therefore it is a
  protected branch and cannot directly be committed to. Please think twice before merging into master and make sure to
  always test your code. More information about the CI/CD Setup can be found
  here: [CI/CD Setup & Planning](https://fluence.fokus.fraunhofer.de/pages/viewpage.action?pageId=23658588)
