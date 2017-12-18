# OpenStreetMap Data Case Study

## Map Area
San Diego, CA, United States

- [https://mapzen.com/data/metro-extracts/metro/san-diego_california/](https://mapzen.com/data/metro-extracts/metro/san-diego_california/)

I am from San Diego, and thus I decided to dive in to the Open Street Map Data for my hometown. I still have familiarity with the main streets and zip codes, and thus have a solid knowledge base to spot any initial errors in the data. 

---

## Problems Encountered in the Map
I downloaded the San Diego street map data in XML form to be parsed by my python script data.py. Give the sheer size of the data, I decided that it was best to extract out a sample of the data, and run it through the python script to spot any initial errors. After parsing though the data there were two main issues I found in the data, Inconsistent Postal Codes, street types being over abbreviated and values containing invalid characters. 

### Inconsistent Postal Codes
There were two main issues with postal codes in this open street map data. First being the tags for the postal code was not consistent, with the two tags zip code and postcode both denoting the postal code of a given node. This problem was an easy fix, and I implemented the code:

```python

if child_values['key'] == "zipcode":
    child_values['key'] = "postcode"

```
Additionally, I found several instances of inconsistent postal codes, such as "CA 92104", and 92010-1407, in total there were 10 postal codes that did not match the uniform 5 digit code with the rest of the data. Using the function below, I was able to convert the zip codes to a uniform 5 digit code. 

```python
def updated_zipcode(child_values,values):
    #update zipcode values to appropriate value
    if values['v'].find('CA') != -1:
        zip_value = values['v'][values['v'].find("CA")+3:]
    else:
        zip_value = values['v'][:5]
return zip_value
```

Upon reviewing all of the Zip Codes in the Dataset, there were all 91--- and 92--- except for two, one was only 3 digits, and 1 was in the Santa Barbra area, which must have been a typo. The top values 

I checked the Santa Barbra Area postal code, and it turns out it is in the ways_tags table with the following script:

```sql

SELECT key, value FROM ways_tags WHERE id = (SELECT id FROM ways_tags WHERE key = "postcode" and value = "93108");

Key, Value
name,"Dept. of Veteran Affairs"
source,"SanGIS Footprints_Nonresidential_SD public domain (http://www.sangis.org/)"
building,yes
street,"Rio San Diego Drive"
TYPE,Office
postcode,93108
building_type,office
OBJECTID,10549
housenumber,8810

```
Turns out this building actually has a zip code of 92108, not 93108, which makes it just one digit off, and thus it was probably a typo. 

After processing, I used the SQL script below to produce the top 10 results for zip codes, all of which are in San Diego County. 

```SQL

SELECT tags.value, COUNT(*) as total 
FROM (SELECT * FROM ways_tags UNION ALL
SELECT * FROM nodes_tags) tags
WHERE tags.key='postcode'
GROUP BY tags.value
ORDER BY total DESC
LIMIT 10;

ZIP, Total
92114,15167
92117,14110
91977,12976
92154,12825
91941,11620
92115,10754
91911,10751
92071,10260
92105,10176
91910,10084
```

### Inconsistent Street Types
In San Diego there turns out to be many different street types, different from the usual Street, Road etc. Examples of these are Cid and Avenida, given the Spanish influence in San Diego. With this in mind, I was able to convert most of the inconsistently abbreviated street types programmatically. Using mapping procedures, I populated the following dictionary to successfully convert most of the street names.
```python
mapping = { "St": "Street",
    "St.": "Street", 
    "Rd.":"Road",
    "Ave":"Avenue",
    "Av":"Avenue",
    "Ave":"Avenue",
    ...
    "Pkwy":"Parkway",
    "Pl":"Place",
    "Prky":"Parkway",
    "Py":"Parkway",
    "Rd":"Road",
    "St":"Street",
    "Wy":"Way"}
```
--- 

### Tag Values Containing Invalid Characters
I initially found 66 values in tags that contained some sort of invalid character, ie:
```python
    PROBLEMCHARS = re.compile(r'[=\+&<>;\"\?%#$@\,\.\t\r\n]')
```
Most of these values were either because they were HTML's or had semicolons in them such as:
'shop':'party;costume'
'hgv:national_network':'Caltrans http://www.dot.ca.gov/hq/traffops/trucks/truckmap/'.
Given most of these values seemed okay, I ignored all forward slashes, as they were mostly attributed to urls, and replaced all invalid characters with a space if they weren't adjacent to a space already. 

### Inconsistent Phone Numbers:
In the data set there were numerous different formats for how the phone numbers where laid out, examples of +1(619)-512-2039 and 1-619-512-2039. In order to remedy this problem and make the phone numbers uniform, I implemented the python function for all phone numbers and fax numbers. 
```python
def fixed_phone(values,child_values):
    #fix phone numbers
    phone = ""
    orig =values['v']
    for i,number in enumerate(orig):
        if phonechars.search(number):
            pass
        else:
            phone = phone + number
    if phone[0] == '1':
        phone = phone[1:]
    phone = "(" + phone[0:3]+") "+phone[3:6]+"-"+phone[6:]
    return phone
```

After running this script, I then checked to make sure that all phone numbers were formatted correctly. The following query yielded the listed results:
```sql

SELECT SUBSTR(value,0,6) as areacode, COUNT(*) as count
FROM nodes_tags
WHERE key= "phone" or key = "fax" 
Group by areacode
ORDER BY count DESC;

areacode,count
(619),156
(858),56
(800),5
(888),3
(760),2
(877),2
(310),1
(562),1
(610),1
(823),1
(855),1
(866),1
```
The top 6 results all make sense, as they are all area codes found in San Diego or 800 numbers. 610 was likely a entry error as the 0 and the 9 are next to each other, and 310 is an area code in Los Angeles, which might be from a person that recently moved. The remaining area codes didn't fit, so I ran a query to figure out what was going on. Two egregiously discrepant results are listed below:

(562),"(562) 077-8619"

(823),"(823) 173-85998"

For the first result, it looks like the 619 area code is at the end of the number, which was in fact due to the original entry being 562-0778 (619), which was a type of error my initial script didn't catch. The second entry, has 1 to many digits, which was an error not caught by my script, but is an invalid phone number entry that can't be fixed without researching the node. 

---

## Data Overview and Additional Ideas
This section will discuss general data aspects for this data set, along with the several high level SQL queries used to evaluate the data. 

### File sizes
```
san-diego_california.osm | 305.1 MB
project3.db              | 10 KB
nodes.csv                | 82.1 MB
nodes_tags.csv           | 84.9 MB
ways.csv                 | 5.1 MB
ways_tags.csv            | 19.5 MB
ways_nodes.csv           | 18.4 MB
```
### Number of nodes

```SQL
SELECT COUNT(*) FROM nodes;
```

1017746

### Number of ways

```SQL
SELECT COUNT(*) FROM ways;
```
88534

### Number of unique users

```SQL
SELECT COUNT(DISTINCT uid)
FROM(
SELECT uid FROM nodes
UNION
SELECT uid FROM ways) a;
```
994

### Top 10 contributing users

```SQL
SELECT uid, COUNT(*) as count
FROM(
SELECT ways.uid as uid FROM ways
UNION ALL
SELECT nodes.uid as uid FROM nodes) a
GROUP BY uid
ORDER BY count DESC
Limit 10;

uid   |count
318696|335145
17490|162958
48060|128338
147510|91622
296869|16884
416346|15927
688027|12997
123633|12641
238349|12147
902727|10606

```
---

## Additional Ideas
### Mobile App for Increased Completeness of Information
This data set is no where near complete. As I was exploring the data I noticed that there were 462 restaurants on the map (note, this does not include fast food establishments etc.) by running the SQL query below:
```SQL
SELECT value, COUNT(*) as count FROM nodes_tags 
WHERE key = 'amenity' AND value = 'restaurant' 
GROUP BY value;

restaurant|462
```


For these 462 restaurants, I was curious how many of them had phone numbers listed. Running the query below I found that only 40 or 8.65% of restaurants had phone numbers listed. 

```SQL
SELECT nodes_tags.key, COUNT(*) as count
FROM nodes_Tags
JOIN(SELECT DISTINCT(id) FROM nodes_tags WHERE value = 'restaurant') a
WHERE nodes_tags.id = a.id AND nodes_tags.key = 'phone'
GROUP BY nodes_Tags.key;

phone|40
```

Running similar queries to the one above, I discovered similar trends with the data. 

* Restaurants with cuisine provided: **65.1%**
* Restaurants with a website provided: **14.0%**
* Restaurants with the opening hour provided: **6.9%**
* Restaurants with vegetarian information provided: **1.3%**

These are all pieces of information that I would consider very important for restaurants. One solution to this lack of information is to implement and app for the mobile device that would use the user's location (lat & long) to submit data for a particular restaurant or business. Select business type: "restaurant" on the app would produce a list on information for the user to input, with each input have strict formatting requirements(which would hopefully limit the amount of variation in a field such as phone number. This would lower the barrier of entry for users to input(and business owners) to input valuable and essential information about places in their immediate surroundings. 

### Further Data Exploration 

#### Most Popular Street Name
```SQL
SELECT value, COUNT(*) as count FROM nodes_tags
WHERE key = 'street' 
GROUP BY value
ORDER BY count DESC
LIMIT 10;
```

```SQL
Broadway|957
El Cajon Boulevard|696
University Avenue|689
Palm Avenue|596
Madison Avenue|595
Central Avenue|586
Manzana Way|575
5th Avenue|549
33rd Street|538
4th Avenue|537
```

#### Number of One Way Streets

```SQL
SELECT key,value, COUNT(*) as count FROM ways_tags
WHERE key = "oneway" and value = "yes"
GROUP BY value;
```
oneway|yes|13822
or **2.6%**

#### Most Common Number of Lanes For Residential Streets
```SQL
SELECT ways_tags.key, ways_tags.value, COUNT(*) as count 
FROM ways_tags
    JOIN(SELECT DISTINCT(id) FROM ways_Tags WHERE key = "highway" and value = "residential") b
WHERE ways_tags.id = b.id and key = "lanes" and type = "regular"
GROUP BY value
ORDER BY count DESC;
```

```SQL
lanes|2|167
lanes|1|27
lanes|3|8
lanes|4|2
```
#### Street With the Most Mexican Food Establishments (YUM!)

```SQL
SELECT nodes_tags.value, COUNT(*) as count 
FROM nodes_tags
JOIN(SELECT DISTINCT(id) FROM nodes_tags WHERE value = "mexican") b
WHERE nodes_tags.id = b.id and key = "street"
GROUP BY value
ORDER BY count DESC
LIMIT 1;
```

```SQL
El Cajon Boulevard|3
```

**Note:** There is a good chance I have been to all 3!


## Conclusion
Processing the data for the San Diego Area was a coming home of sorts, however I did find that a lot of the data was incomplete (as evidenced by the restaurant data example). Implementing a script that pulls from sources such as Yelp!, along with a script similar to the data.py, could allow for cleaned data being contributed to the OpenStreetMap.org database.  
