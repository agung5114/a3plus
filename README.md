# a3plus - GrabDCU+

Our solution for GrabForGood HAckathon consist of two apps, with the main app (grabdcu) providing features for the user, 
while the other one (grabfoodcv) focus on the use of machine learning to handle complex problems and performing analytics.
Furthermore, we also build swagger for communicating with grab-api, although the access is limited to sample data, 
we can analyse the data structure so that we can ensure our solution will be feasible to integrate with current grab system.

Prerequisite

Install Python version > 3.6;
Install Virtual Environment;
Create virtual environment.

To run the main app (grabdcu) do the followings:
  1. git clone or the repository or download the code
  2. install dependencies required with pip install -r req.txt
  3. make database migration with python manage.py makemigrations
  4. migrate the database with python manage.py migrate
  5. run app with script in terminal: python manage.py runserver
It has been deployed online and can be accessed at: http://a3plus.mofdac.com

For the grabfoodcv app, the steps are:
  1. git clone or the repository or download the code
  2. install dependencies required with pip install -r req.txt
  3. run app with script in terminal: streamlit run stapp.py
It has been integrated with the main app and can be accessed at: http://a3plus.mofdac.com

For the API swagger
  1. Running Virtual Environment;
  2. Install libraries as listed on requirements.txt;
  3. You can run the API on wsgi with command flask run;
  4. The API will run on port 5000 if you run it on local;
  5. The API Specification could be accessed on localhost:5000/apidocs.
As for the deployed online app, it can be accessed at: http://contoh-rest.herokuapp.com/apidocs

We also provide android application viewer to access the grabdcu main application
simply follow the steps below:
  1. download grabdcu.apk file
  2. install the app to your android phone/ tablet
  3. open the app
