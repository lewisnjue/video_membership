1. video 
    - host ( youtube - private video -> udacity)
                -> vimeo, wistia 
                -> self hosted - nginx
    - analytics 
        -> lot of data ( this requres a non relational databases ) -> cassandra 
        



2. members 
    - sign up 
    - login 
    - rember things 
    - email verivication 
    - payments 

```py

q = user.objects.all()

for user in q: 
    print(user.email,user.user_id,user.password)



```


```
# what i want is to imprement my own method to do the following and use it as following 

user.create_user -> to create a new user intead of the defalut one of user.create(**args) -> this is not good for the  verification and password encryption and also for email 
so we need to create our own method here 



```

```py


import pytest 
from app import db  
from app.users.models import User

@pytest.fixture(scope='module')
def setup():
    session =db.get_session()
    yield session
    q = User.objects.filter(email="test@gmail.com")
    if q.count() !=0:
        q.delete()
    session.shutdown()


def test_create_user(setup):
    User.create_user(email="test@gmail.com",password="tesing123")




```
the setup function here is a pytest fixture , whih allows you to define a setup and teardown logic that can be resued in multiple tests. 

here is step by step breakdown of how it works 

1. scope : 
- scope='module' : this means that the setup fixture will be run once per module. any test in this module taht requrest this fixture will use the ame instance created here , rather than creating a new once each time . this is useful for creating resources that should persist across multiple test. 


1. session creation:
- session = db.get_session() : this intialiates a session for use in tests . this session is then passsed to any test function that can use the setup fixture . 


1. yield statement:
- yield session : this effectivery returns the session to any test fuction that uses the setup fixture . after yeild ,pytest will proceed with the test functions.


1. teardown:
- after test run , any code after yeild acts as teardown logic, hre , teh code checks if a suer with the email 'test@gmail.com' estis , deletes it if found , and then shuts down the session wit session.shutdown() to clearn up the database connection . 


so , in summary , setup:

- creates a session for testing 
- provides it to test fucntions 
- cleans up any test data and cloeses the session after tests run . 

this setup helps ensure a consisntesnt test enviroment by cleaingin up any temparray test data after each test . 

