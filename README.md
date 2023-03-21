# mony

In this file I'll be describing what I've made and what files do what.

## Distinctiveness and Complexity
I think this project is good, because it satisfies all the requirements.
It has JavaScript on the front-end, Django on the back-end and is mobile-responsive. I was forced to learn React to make this web-app, learn how to make a REST backend API with Django and also learn Nordigen's API and how it worked.
It was definitely challenging, because it was the first time coding with these resources.

## How to run Mony
Make a Nordigen account here -> https://nordigen.com/en/.
Sign up for an account and create an secret ID and secret KEY here -> https://ob.nordigen.com/user-secrets/
Once you have the secret id and secret key you need to set them to the environment variables before running Mony.
With a linux terminal you can do *export secret_id=YOUR_SECRET_ID* and *export secret_key=YOUR_SECRET_KEY*. 
Now you should be able to run the web-app Mony.


## What I've made
I've made a personal finance app using React for the front-end, Django for the backend and Nordigen banking API.
This webapp is made to have quick and easy insights in your monthly spendings. 
You can connect your banks using the nicely made interface and it will load all th transactions from all the connected banks.

Using this data you can add categories to each transaction, which will be refrected in the diagrams where you can see multiple diagrams for your spending.

## How have I made this?
So there are three main components to this app: the React front-end file, the back-end API handler, and the 'normal' back-end.

### The 'normal' back-end
So this is the **mony** django app. In this app there really isn't a lot of interesting stuff happening. It contains the backend for the general frame to work.
This means functions like rendering all the front-end directories within **views.py** and other implementations including logging in/out, registration and admin installation.

### The back-end API handler
This was something really new to me that I got to explore during this project. Basically this back-end app, which is called **bank_api** in the django apps is responsible for the front-end to back-end requests. Basically the front-end sends a request e.g. to get all transactions, the backend will request this info from the Nordigen API and will return that data back to the front-end. It is too much to go over each function I made for this app. Everything can be found in the **views.py** file of the **bank_api app**. Something interesting that I got to work with aswell is serializers and the django rest framework. To sum up what this app does again is, the app handles all requests done by the front-end regarding bank, transaction and category data. It requests it from the Nordigen API and formats/saves it, so the front-end (but also the back-end) can work with it.

### React.js front-end
And now my favorite part, React. Before starting this poject I aven't really coded in React, but found it a ton of fun!
Th React file can be found in *mony/static/mony/App.js*. Again there is a lot to explain about this app, but I'll explain it it broad terms what happens. The App has four different *main* components: GoogleDiagrams, TransactionHistory, TransactionCategory, ConnectBank. Each of them serve a different purpose. The main App combines them all together into a working webapp. 

**ConnectBank**: It lets the client connect their bankaccount to the **mony** account.
**TransactionCategory**: Lets the client add/remove categories for their transactions
**TransactionHistory**: This gathers all clients bank transactions and displays them on the site
**GoogleDiagrams**: This makes nice diagrams of the data of the previous components.

There is also some other functions like **accessTokenHandler**, which basically just make sure that the cookies within the clients browser are always good and up-to-date. Within this *App* and it's child components there is a ton of fetch requests going to the back-end to make sure everything gets updated when something changes and everything works. The *React.js App* and *bank_api* go hand in hand in this project.

The most difficult part about this project was learning React.js for sure. I was totally not used to the way React works. What was very difficult is the debugging, making the coding structure and making things efficient within the code.

I hope you guys like my project *mony*
