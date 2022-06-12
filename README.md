# a3plus

Our solution for GrabForGood HAckathon consist of two apps, with the main app (grabdcu) providing features for the user, 
while the other one (grabfoodcv) focus on the use of machine learning to handle complex problems and performing analytics
To run the main app (grabdcu) do the followings:
  1. git clone or the repository or download the code
  2. install dependencies required with pip install -r req.txt
  3. make database migration with python manage.py makemigrations
  4. migrate the database with python manage.py migrate
  5. run app with python manage.py runserver
