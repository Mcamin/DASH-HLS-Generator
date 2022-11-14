# DASH-HLS-GENERATOR

This project offers a simple config-file based approach to prepare streaming media. It greatly simplifies the process of
using FFmpeg for both VOD and live content.
##Note 
- __The configs were only tested using all the available attributes on Windows. Removing some attributes might cause issues when
generating the files.__
- __The current setup generates 3 representations / streams for the passed configs. This will be configurable in the future__
## TODO:
- [ ] Add filter capabilities to draw a box with video details 
- [ ] Set up the representations shuffle process (to force bitrate fluctuation)
- [ ] Add option to delete local generated file
- [ ] Fix streams in hls generated files 
- [ ] Check mp4box and GPAC for generating HLS Dash  compliant streams 
- [ ] Check shaka packager and streamer and how they do generate multi period content

## Installation & Usage

### Pre-Requisites

- [Anaconda](https://www.anaconda.com/) is installed
- [FFMPEG](https://ffmpeg.org/) is installed 
- An environment with Python 3.7 or greater installed 
- [Mongodb](https://www.mongodb.com/) is installed [optional]
### Setup

##### 1. Clone the project and install all needed dependencies.

```bash
# Clone the project
git clone git@gitlab.fokus.fraunhofer.de:dashcenc/dash-hls-generator.git
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
MONGO_URI="The Mongo URI"
MONGO_DB="The database to use"
OUTPUT_ABSOLUTE_PATH= "The output absolute path"
```

Set the environment variables according to your local setup.

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are the amazon needed credentials to access the bucket.
    If not passed the files will be kept locally given output folder in the configs
- `BUCKET_NAME` is the name of the bucket setup on amazon to be used for storing and delivering content.
- `FFMPEG` is the path to the ffmpeg binary.
- `MONGO_URI` and `MONGO_DB` are the needed config to save the configs to the database.
    If not passed the files will be saved locally in the given output folder in the configs
- `CLOUDFRONT_BASE_URL` is the CDN url used to serve the streaming media. This is used only if AWS credentials is passed 
- `OUTPUT_ABSOLUTE_PATH` The absolute path to be used fo generating the files (examples : [Windows: 'C:\\media\\, Linux: '/media/'])

and cloudfront is configured.  



### Config Documentation
The app takes a json file containing the configuration to be used to generate media streams. 

The config files should contain at least one of these attributes: `hls` or `dash`. 

The `hls`/`dash` attributes should be an array of objects defining the different configs to use to generate the media 
streams.

For more details, check the documentation of the available attributes that can be used in the table below or the example 
config file under [templates](./templates)

| Attribute    | Description |
| ----------- |  ---------| 
| input_file    | The input file to use to generate media streams |
| fps | The number of frames per second    |
| gop_size  | The GOP size   |
| pixel_format  |  The pixel format  | 
| codec_video        | The video codec to use  | 
| codec_audio       | The audio codec to use |
| bitrate_audio      | The audio bitrate | 
| audio_channel      | The audio channel |
| audio_rate     | The audio rate |
| sc_threshold | The scene change threshold |
|keyint_min | The minimum length of the GOP |
| preset | The preset to use|
| output_path |The s3 path where the files will be uploaded|
| use_template* |Enable (1) or disable (0) use of SegmentTemplate instead of SegmentList.|
| use_timeline* |Enable (1) or disable (0) use of SegmentTimeline in SegmentTemplate.|
| segment_duration* |Set the segment length in seconds |
| init_seg_name* |DASH-templated name to used for the initialization.|
| media_seg_name* |DASH-templated name to used for the media segments.|
| adaptation_sets_fmt* |Assign streams to AdaptationSets|
| hls_time** |Set the target segment length|
| hls_playlist_type** |Emit #EXT-X-PLAYLIST-TYPE:VOD in the m3u8 header|
| hls_flags** | Pass hls specific flags |
| hls_segment_filename** |Set the segment filename.|
| strftime_mkdir** | Create all subdirectories which is expanded in filename.|
| stream_filename** |The streams filenames template |
__`**` denote to an hls specific attribute__
__`*` denote to a dash specific attribute__

More details about the available attributes can be found in the references below. 

### Docker 
To be added 
### References: 
- http://underpop.online.fr/f/ffmpeg/help/dash-2.htm.gz
- https://ffmpeg.org/ffmpeg-formats.html#dash-2
- https://ottverse.com/mpeg-dash-packaging-using-gpac-mp4box-live-vod/


### Things to consider

- This project follows the GitFlow Workflow, with features and release branches. Learn more
  here: [GitFlow Tutorial](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- Merges to the `master` branch automatically trigger a deployment to the staging environment, therefore it is a
  protected branch and cannot directly be committed to. Please think twice before merging into master and make sure to
  always test your code. More information about the CI/CD Setup can be found
  here: [CI/CD Setup & Planning](https://fluence.fokus.fraunhofer.de/pages/viewpage.action?pageId=23658588)

### Changelog
#### 1.0.0 - [07.11.2022 - 11.11.2022]
###### Added
- [X] Added documentation
- [X] Added s3 support to store files 
- [X] Added mongodb support for storing configs

####  [Unreleased- Template]
###### Added
###### Changed: Feature change
###### Fixed:  Bug fix
###### Deprecated: New deprecation
###### Removed: Feature removal
###### Security: Security fix
###### Performance: Performance improvement
###### Other: Other