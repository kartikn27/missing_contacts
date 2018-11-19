# MISSING CONTACTS
Copy missing contacts from the csv to contacts API endpoint

## Steps to Run:
### 1. Decompress/Unzip contacts.csv.bz2
By default, it should be decompressed as **contacts.csv**

If not, rename the files as **contacts.csv**

It's location should be **/ingestion_files/contacts.csv**

### 2. Install the dependencies using following command
```
pip install -r requirements.txt
```
***xlrd*** - Dependency to access XLS(excel) files

***Pandas*** - Data manipulation library

***validate_email*** - To check email's validity

### 3. Run the application using the follwing command
```
python main.py 'Mining, Quarrying, and Oil and Gas Extraction' 'Transportation and Warehousing' 'Professional, Scientific, and Technical Services'
```

## Application Workflow
1. The application is invoked through command line argument, which accepts three required sectors.

2. These sectors are searched in **/ingestion_files/2-6 digit_2017_Codes.xlsx** and their corresponding sector ids is obtained.

3. These parent sector ids are two digit numbers. So to obtain the industry which belongs to these sectors, all the sectors which start with the obtained two digit sector ids are considered are the industry names of the contact.

4. From the filtered contacts, first_name, last_name, email, industry_name, company_name form the part of the attributes object.

5. To find the supervisor relationship, the supervisor email is searched using the ***/contacts/search?email=*** GET request and for the obtained request, the contact id is added to he relationships object.

6. The POST new contact payload consists of attributes and relationships objects from steps 4 and 5. The contacts are POST to api ***/contacts***


## Assumptions and Observations
1. All the sectors and their ids are obtained from [2-6 digit sector ids](https://www.census.gov/eos/www/naics/2017NAICS/2-6%20digit_2017_Codes.xlsx).

2. If the email of the contacts id **/ingestion_files/contacts.csv** is NULL/Blank/Not found, that contact is skipped.

3. Any sector in **/ingestion_files/2-6 digit_2017_Codes.xlsx** whose sector id, which matches with the first two digits of the parent sectors(obtained from command line) are the industry names of the sectors.

4. Contacts with similar email id are passed through POST request.
