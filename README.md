# a3plus - GrabDCU+

Our solution for GrabForGood HAckathon consist of two apps, with the main app (grabdcu) providing features for the user, 
while the other one (grabfoodcv) focus on the use of machine learning to handle complex problems and performing analytics
To run the main app (grabdcu) do the followings:
  1. git clone or the repository or download the code
  2. install dependencies required with pip install -r req.txt
  3. make database migration with python manage.py makemigrations
  4. migrate the database with python manage.py migrate
  5. run app with script in terminal: python manage.py runserver

As for the grabfoodcv app, the steps are:
  1. git clone or the repository or download the code
  2. install dependencies required with pip install -r req.txt
  3. run app with script in terminal: streamlit run stapp.py
