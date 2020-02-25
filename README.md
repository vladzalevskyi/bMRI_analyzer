# bMRI_analyzer 
## Overview
**bMRI_analyzer** - a demo website which provides doctors and nurses with a Patient Control Systems and an ML module for automatic brain MRI image tumour classification and segmentation.

Developed as coursework for my 3rd year of study, it combines the knowledge I received during my Web Programming, Distributed Systems, Python and DBMS courses. It's a containerized web application ready for deployment and scaling. Following technologies were used during its development:
- Python
- Flask
- FastAI
- Keras & Tensorflow
- SQL-Alchemy
- OpenCV
- MySQL
- HTML/CSS/JS
- Docker
## Structure
Since the application is deployed via docker-compose, its structure can be viewed in the `docker-compose.yml` file. The general structure is the following:
![Application Structure](https://github.com/Vivikar/bMRI_analyzer/blob/master/readme_img/Untitled%20Diagram.png)

DB structure can be described by:

Data Flow Diagram
![Data Flow Diagram](https://github.com/Vivikar/bMRI_analyzer/blob/master/readme_img/data_flow.png)

Entity Relation Diagram
![Entity Relation Diagram](https://github.com/Vivikar/bMRI_analyzer/blob/master/readme_img/entity_rel.png)

## Deployment
To run  web application locally all you need is to clone the repository and run 
```
$ docker-compose up --build
```
It will automatically install all dependencies and sequentially run all the containers needed for applications work.
## Exaples of work
Few screenshots describing application work
Homepage
![Homepage](https://github.com/Vivikar/bMRI_analyzer/blob/master/readme_img/homepage.png)

Patients list
![Patients](https://github.com/Vivikar/bMRI_analyzer/blob/master/readme_img/patients.png)

Image analysis results Page
![Image analysis results Page](https://github.com/Vivikar/bMRI_analyzer/blob/master/readme_img/img_anal.png)
