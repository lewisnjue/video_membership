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

