### Table of Contents
[Blog Examples](https://github.com/Kibrael/mwo_data#blog-examples)  
[Instructions](https://github.com/Kibrael/mwo_data#instructions)  
[Repository Structure](https://github.com/Kibrael/mwo_data#repository-structure)  

## MechWarrior Online Match Score Data Project
Disclaimer: This project is not affiliated with [PGI](http://piranhagames.com/) or [MechWarrior](https://mwomercs.com/).
### Project Goal:
This project aims to construct a dataset based on game results from MechWarrior online. 
Match results will be combined with mech weights to facilitate analysis of tonnage deltas 
between teams.

The resulting dataset will contain nearly 600 images converted to pipe delimited text files
and mech tonnage by variant in the same format.

The combination of these datasets will allow statistical inference into matchmaking engine
priorities.

## Blog Examples
Please see [this link](link to blog) for a discussion on the use and results of these code files.	

To run the scripts below begin in the Python sub folder.

- [Whole screenshot](Python/whole_screenshot_example.py): Code for sending the entire test image to the AWS Rekognition API. This is a test of the return and is not optimal for dataframe construction.  
`python whole_screenshot_example.py`

- [Horizontal slicing](Python/single_row_example.py): Code for sending horizontal slices of the test image to the AWS Rekognition APi. This example includes both a single row return as well as an example on assembling a dataframe from multiple API calls. This method optimizes cost at the expense of data cleaning time.
`python single_row_example.py`

- [Horizontal and vertical slicing combination](Python/split_screenshot_example.py): This example slices an image into individual cells and sends each cell individually to the Rekognition API. This method optimizes for data cleaning time at the expense of cost.
`python split_screenshot_example.py`

- [Dataframe output from OCR](https://github.com/Kibrael/mwo_data/tree/master/output/blog_files/dataframes) contains text files of dataframes produced by the example code files
- [Images of dataframe output from OCR](https://github.com/Kibrael/mwo_data/tree/master/output/blog_files/df_screenshots) contains images of the dataframes produced by the example code files  
*Analysis powered by [kite](kite.com)*



## Instructions
- This project relies on [Python](https://www.python.org/downloads/) 3.7
- Install [requirements](requirements.txt)
- Set up your [AWS credentials](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html)
- running web scrape code from the Python subfolder will generate a list of mech variants and tonnages: `python run_mech_scrape.py`
- running code for single screenshot: TBD
- running code for many screenshots: TBD


## Repository Structure
- image data
	- data source (screencapture)
- [Web Scraping](Python/run_mech_scrape.py): Uses the [mech_scrape](Python/lib/mech_scrape.py) class to gather tonnage for each mech variant in [MechWarrior Online](https://mwomercs.com/).
- [test data](https://github.com/Kibrael/mwo_data/tree/master/data/test_data) contains image files sliced from screenshots. Some images have been resized and/or threshed in greyscale.
- [image data](https://github.com/Kibrael/mwo_data/tree/master/data/images) contains the test image used in the examples. A full set of screenshots is not currently available.
- [image slicer](https://github.com/Kibrael/mwo_data/blob/master/Python/lib/mwo_image_slicer.py) converts screenshots to dataframes which can be saved as text. Two methods, horizontal, and a combination of horizontal and vertical slicing are available. The combination of horizontal and vertical slicing yields better results but requires more time and costs more in API calls.
- [initial dataframes]() contains the initial dataframe output from screenshot conversions.
- [cleaned dataframes]() contains dataframes that have been cleaned of errors created during the OCR process.
