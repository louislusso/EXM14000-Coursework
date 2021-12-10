# README
This project can be found [Here](https://github.com/louislusso/EXM14000-Coursework) 
## Overview 
Thi project is a simple personalised covid dashboard. Dashboards are automated systems that help visualise input data streams. This dashboard application will coordinate information about the COVID infection rates from the Public Health England API and news stories about Covid from a given news API.
The dashboard will need to run continuously and respond to events. These events can either be scheduled by the developer or triggered by user inputs.

## Introduction:
        This program is a user freindly interface used for receiving the latest covid-19 data from the UK goverments covid API
        The purpose of this project is so that users can input the locations they want to know coivd-19 statistics about into the config and be able to access an easy GUI where the total deaths, current hospitalisations and the number of new covid-19 cases in the last 7 days. You are also able to view relivant news articles to the covid-19 topic and schedule updates to both the data and news articles at any time.

## Prerequisites:
        The program was developed in python 3.7.9 with spyder on a windows machine 

## Installation:
        For this project to work you will have to install...
            uk_coivid19 -> pip install uk-covid19
            flask -> pip install flask
            newsapi -> pip install newsapi-python
        I have also used these extra modules:
            csv
            jsom
            sched
            time
            lodgging
            threading

## Getting Started:
1. Download the project at - link
2. Go to the newsapi website and get a free API key - link
3. Install the relivant packages mentioned above via pip (uk_covid19, flask and             newsapi will almost definatley not be preinstalled)
4. Enter all the relivant information in the config file 
5. run the project from the covid_html_handler.py module
6. You will then be able to open your browser and access the interface by entering http://127.0.0.1:5000/index

## Config file help

For the filepaths do not include a filename 

1. csvFilenameFilepath - filepath for the test csv 'nation_2021-10-28'
2. csvTopFilenameFilepath - filepath to save the csv for the data for the area at the top of the user interface
3. csvBottomFilenameFilepath - filepath to save the csv for the data for the area at the bottom of the user interface
4. Toplocation - name of the area at the top of the user interface
5. Toplocation_type - the location type of the area at the top of the user interface
6. Bottomlocation - name of the area at the bottom of the user interface
7. Bottomlocation_type - the location type of the area at the bottom of the user interface
8. covid_terms - list of terms used to filter the news results
9. api_key - the news API key used to access the newsapi module
10. static_foler_name - location for the static foler
11. log_file_location - log file location
12. log_file_location

### Location type help
        LTLA - Lower Tier Local Authority
        MSOA - Middle-ayer Super Output Area
        Nation - Different nations of the UK
        NHS Region - Healthcare regions of England
        NHS Trust - Healthcare trusts of England
        Overview - For the UK
        Region - avaliable for england
        UTLA - Upper Tier Local Authority 

More info on the Covid_19 API can be found in the [Developers Guide](https://coronavirus.data.gov.uk/details/developers-guide)

## Special Thanks To:
        Dr Matt Collison - University Of Exeter 2021 - m.collison@exeter.ac.uk
        Dr Hugo Barbosa - University Of Exeter 2021 - h.barbosa@exeter.ac.uk


## Licence:
 ### Copyright <2021> <Louis Andrew Lusso>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.







