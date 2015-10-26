# yeg-oral-history
SoundCloud comment scrapper for Open Edmonton's Oral History Project.

### Overview
This is a SoundCloud comment scrapper for Open Edmonton's Oral History project. A group of volunteers went through the various interviews and added keyword tags. These keyword tags are associated with certain times during the interview. This scrapper extracts these keywords from the comments and creates a database. The database can be exported to a CSV file for easier analysis.

### Requirements  
It is assumed you have Python 2.7 installed on your system with ``pip`` installed as well.

### Running the Project
1. pip install -r requirements.txt
2. python manage.py migrate

The first command will install the prerequisite Python packages. The second command will run the scrapping command
