# missing_contacts
Copy missing contacts from the csv to contacts API endpoint

## Steps to Run:
### 1. Decompress/Unzip contacts.csv.bz2***
By default, it should be decompressed as **contacts.csv**
If not, rename the files as **contacts.csv**
It's location should be **/ingestion_files/contacts.csv**

### 2. Install the dependencies using following command
```
pip install -r requirements.txt
```

### 3. Run the application using the follwing command
```
python main.py 'Mining, Quarrying, and Oil and Gas Extraction', 'Transportation and Warehousing', 'Professional, Scientific, and Technical Services'
```
