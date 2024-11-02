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



in web development , cookies are small pieaces of data stored on the users device by their web browser as they interact with websites . cookies play a key role in maintain a suers session , tracking site preferences and anabling a personiized web experience 

here is a breakdown of how cookies work, including types and common use cases 

## WHAT COOKIES ARE AND HOW THEY WORK 

a cookie is essentailly a text file ontainng information in name vaue paris , such as user_id =123. when a suer visits a website , teh web server can create a cookie and send it to the users broswer , which stores it . every time the user revistis the site , theri brwoser sends the cookie back to the server , allowing the sit t e rember the user . 


#### BASIC STEPS : 

- user visits a website . if the site need to save data , it sends a set-cookie header in the http response. 

- browser stores the cookie : the browser keeps that cookie data , either until it expires or is manually crealed . 


- browse sends cookie on subsequesnt requests : each time the user revistis the site , teh browser includes the cookie data in the http requst header , allowing the server to rember previous information . 




## TYPES OF COOKIES 

there are different types of cookies based on their purpose and lifespan: 

- sesion cookies : these are tempoarry cookies that expire once the user closes the browser . thery ofen used to keep users loged in during their seesion or rember temporarry selections 

- persistent cookies : these  remain on the users device for a set period ( determed by teh Expires or Max-Age) attribute . they are useful fo rrembering login ifnoramion , language preferences or user personaliion across sessions . 


- first party cookies : created by the website ther user is currentry visting , these are typically sued for core site functionaliry tlike tracking logged in status or string perfernces . 

- third party cookies : created by domains other that the user is currently vising , these are typically used by adversisers and analytics companies to track users across multiple sites , providing data for targeted adversing . 


### COOOKIE ATTRIBUES 

cookies comes with various attribues that control how they behave : 

- Expires / Max-Age : define how long the cookie is stored . Expres is specific data , while Max-Age specifies a nubmer of seconds . 

- Domain : Specifies the domain where the cookie is valid . subdomains can also be specified . 

- Path : limes where teh cookie is sent within the website . for example setting Path=/user would only send the cookie on request within the /user path . 

- secure : ensure that the cooie is only sent over https connectison , protecting it from eaverpropping . 

- httpony : prevent javasript from accessing the cookie , helping protech it from cross site scripting (xss) attacks .


- samesite : restrics cookies from being sent alogn with cross site reqeust . can be set of strict , lax or none , which adds an exra layer of pretection againist cross site request forgery attacks . 


### COMMON USE CASES FOR COOKIES 

cookies have several improrant use cases , especially for user exerience and session management . 

- user sessions : cookies are ofetn used to maintain user lgin sesesion so that users remain logged in as they naviage different pages . 

- personalizaion : preferences like language settings , themes 
- shopping carts : for ecommerce sites , cookies help keep track of itesm added to a cart even before the user logs in . 

- analtcs and tracking : cookies enable tracking of use behaviou on a site or across sites , allowing analsytics and targetd adverstinng 

 when we add our authenticaion middle ware , this will allow us to be able do do things like 



print(request.user) and things like print(request.user.is_authenticated)


