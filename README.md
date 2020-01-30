# bMRI_analyzer 
## Overview
**bMRI_analyzer** - a website with all the supporting infrastructure that provides its users with a Patient Control System and a specified module for automatic MRI image analysis.

Developed as coursework for my 3rd year of study, it combines the knowledge I received during my Web Programming, Distributed Systems, Python and DBMS courses. It's a containerized web application ready for deployment and scaling. In the process of creating it following technologies were used:
- Python
- Flask
- Keras & Tensorflow
- SQL-Alchemy
- OpenCV
- MySQL
- HTML/CSS/JS
- Docker

## Deployment
To run  web application locally all you need is to clone the repository and run 
```
$ docker-compose up --build
```
It will automatically install all dependencies and sequentially run all the containers needed for applications work.
