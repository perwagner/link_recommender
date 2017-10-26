# Link recommendation (user based collaborative filtering)
Using the 'Anonymous Microsoft Web Data Data Set' [here](http://archive.ics.uci.edu/ml/datasets/Anonymous+Microsoft+Web+Data) as training data, the app provides an API endpoint for getting link recommendations given a user id. In case of a new user without any link history, the API returns a list of the 5 most visited sites.

## Install and setup
### Docker
The app can be run locally with docker-compose using the command:
```
>> docker-compose up
```
The API will be available on 'http://localhost:5000/api/v1'.

### Non-docker
The system is build on Python 3.6. Install dependencies in a virtualenv:
```
>> virtualenv venv -p python3.6
>> source venv/bin/activate
>> pip install -r requirements.txt
>> FLASK_APP=app-api.py flask run
```
## Usage
The API exposes two endpoints:
* /status
* /recommender/<user_id>
They can be reached locally via: 'http://localhost:5000/api/v1/status' and 'http://localhost:5000/api/v1/recommender/<user_id>', where <user_id> is an integer representing a specific user.

The recommender endpoint might tage a few seconds to return data, as the user based collaborative filtering algorithm is recalculated on every request and is not especially efficient.

## Testing
Pytest is used for running the tests. All tests can be run via:
```
>> pytest tests/ -v
```
Code coverage can be displayed with
```
>> py.test --cov=app 
>> py.test --cov=app --cov-report html
```
If HTML output is generated, this will be available under the /htmlcov directory. Be mindfull, that using coverage increases the excecution time of the test suite.

## Method choice reasoning
### Why user based and not item based collaborative filtering?
Given the data available user based collaborative filtering is easy to implement and allows the system to return recommendations based solely on who the user is. The alternative, to use item based, would likely work by having the user go to a webpage, and given this webpage the system would recommend other webpages. This could be implmenented, but hasn't been done for this system. 


### Issues with user based collaborative filtering
* As the system essentially is build on users' past behavior, the data might have an 'expiry date' in the sense that peoples' tastes and interests change over time. Thus, old data might not be relevant to use as training data (however, the dataset doesn't include timestamps). Additionally, if several real people use the same profile, this might pollute the user data.
* The list of people is likely to grow over time (while the list of webpages probably has some upper limit). This will lead to an increase in the computational burden required to calculate the correlation matrix of similar users (doesn't scale well).
* Given the system depends on real people, it can be 'tricked' or gamed (like Shilling attacks).


# Resources
* https://medium.com/ai-society/a-concise-recommender-systems-tutorial-fa40d5a9c0fa
* https://blog.dominodatalab.com/recommender-systems-collaborative-filtering/
* http://surprise.readthedocs.io/en/stable/getting_started.html
* https://blog.statsbot.co/recommendation-system-algorithms-ba67f39ac9a3
* http://www.salemmarafi.com/code/collaborative-filtering-with-python/
* https://cambridgespark.com/content/tutorials/implementing-your-own-recommender-systems-in-Python/index.html
* https://www.analyticsvidhya.com/blog/2016/06/quick-guide-build-recommendation-engine-python/
* http://guidetodatamining.com
* http://blog.untrod.com/2016/06/simple-similar-products-recommendation-engine-in-python.html
