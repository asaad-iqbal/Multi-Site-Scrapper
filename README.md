#MULTI SITE SCRAPPER

requirements:
install Python version >= 3.6 (3.9.5 version preferrable, I used)
selenium ChromeDriver version used 96.0.4664.45 (already places in selenium folder)
optional: SQLLite browser for accessing sqllite db file in database folder
Note: python already comes with sqllite3 support and library does not need to be installed

Install all libraries using this command (after opening cmd/terminal in project directory):
pip install -r requirements.txt

How to run:
1) Navigate to project main directory
2) Open scrapper_v1.py
3) Change excel_ bit to True if want to save in excel
4) Change db_ bit to False if dont want to save in database
5) Change append_ bit to False if want to overwite table everytime 
   while saving to database (default True, append to already existing data, removing duplicate data)
6) Run command in terminal or IDE (I used VS code): 
   python scrapper_v1.py
   If upper command doesnt work then:
   python3 scrapper_v1.py
   If that doesn't work then install proper libraries
7) Provide whole url to be scrapped (urls only works for provided 4 websites, search url should work for all searches)
8) Database tables store in database folder in scrapper.py database (duplicate entries remove automatically)
8) Excel results store in excel folder
   