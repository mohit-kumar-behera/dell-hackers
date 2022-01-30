# Tracker

## Installation

pip install tracker

## Documentation

**This package is used to track changes made in a file,currently we only support json file format but in future we will make it work for more file formats.**

How to use it:- <br />
For each file to track you need to initialize an object of the tracker class like so:- <br />
  
  ```
	trackObj = Tracker(BASE_DIR, audit_filename, table_pk_name)
  ```
**BASE_DIR:** The path where all the deltas of the file should be stored. <br />
**Audit_filename:** Name of the file that has to be tracked. <br />
**Table_pk_name:** primary key of the file ,that is any way to uniquely identify each record of the file 

You also need an firebase account for storing the deltas so create a firebase account and take the logging information. Make sure to make the accessibility of the storage global.
After that just initialize the storage as shown below. <br />

```python
TRACKER.initialize_firebase_storage(firebaseConfig)
```

FirebaseConfig is a dictionary like so:- <br />

```python
  firebaseConfig={"apiKey": "abc",
    "authDomain": "abc",
    "databaseURL": "abc",
    "projectId": "abc",
    "storageBucket": "abc",
    "messagingSenderId": "abc",
    "appId": “abc",
    "measurementId": "abc"}
  
  ```
 Replace abc with your values.

Now you are ready to track your files as per your need, now to track any changes made you just need to pass the old and new values of the changes record as shown below. <br />

```python
trackObj.track(oldObj,newObj)
```

**oldObj:** a json object containing the information of previous state of the record that has undergone a change <br />
**newObj:** a json object containing the information of the current state of the record that has undergone a change.

**The different  functions needed to get the deltas are described in details below:**

 1. **get_all_audits():** this function will return all the deltas of the file, made till date in a json file format.
 2. **audit_of_today():** This function will return the deltas of the file that one has made today in json format.
 3. **audit_of_date(d, m, y):** This function will return the deltas of the file that one has made in a particular date, month and year. Here d represents day, m represents month and y represents year in number.
 4. **audit_from_date(d,m,y):** This function will return the deltas in a file that one has made from d/m/y until now. Remember d is the integer that represents day,m represents the month and y represents the year.
 5. **audit_between_date(sd,sm,sy,ed,em,ey,endpoints=False):** This function returns the deltas of the file that has happened between sd/sm/sy to ed/em/ey (sd: starting day, sm: starting month, sy: starting year, ed: ending day, em: ending month, ey: ending year). Endpoints is a parameter that represents whether you want all the deltas or just the final deltas between the endpoints. If endpoints is false(which is its default value) then the function will return all the deltas made between the two dates in a json format else if it is true then it will just compare the initial state of the file at sd/sm/sy and compare it with the final state of the file at ed/em/ey and give you the deltas in a json format.
 6. **audit_by_id(id,sd,sm,sy,ed,em,ey):** Returns the json file containing changes made in a particular id between the date ranges sd/sm/sy and ed/em/ey (sd: starting day, sm: starting month, sy: starting year, ed: ending day, em: ending month, ey: ending year).
 7. **audit_by_operation(operation,sd,sm,sy,ed,em,ey):** Returns the json file containing the changes made of a particular operation (updated,inserted,deleted)  in the file between sd/sm/sy to ed/em/ey (sd: starting day, sm: starting month, sy: starting year, ed: ending day, em: ending month, ey: ending year). 
