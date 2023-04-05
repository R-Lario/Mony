# mony

Mony is a personal finance app that allows it users to track their monthly expenses. Users can connect European banks to the webapp and the app will show all the transactons for the connected banks in the past 90 days. With those transactions, the users can categorize them and see their monthly expenses per category. This webapp could be usefull to people who want to analyze their expenses in order to be more efficient with their mon(e)y. 

## Distinctiveness and Complexity
This project is built using JavaScript (React) on the front-end, Django on the back-end and is mobile-responsive. I was forced to learn React to make this web-app, learn how to make a REST backend API with Django and also learn Nordigen's API and how it worked.
It was definitely challenging, because it was the first time coding with these resources. The most challenging thing I faced with this project is getting the hang of React. With other projects I have never used React, so this was a pretty big step. Another thing which was quite tricky was the fetch requests to the back-end api and making sure the code ran asynchronous. Besides that what I needed to wrap my head around is the `useEffect` and `setState` functions. This way of programming I've never encountered and was definitely challenging. 

At some point I tried to `setState` and run some code with the updated state on the next line. Well that didn't work, because the state didn't update by then yet, which ment I really needed to use `useEffect` to do what I intended to do. This however wasn't easy and I had to rewrite my whole React components code.
Another thing with React that I struggled with is connecting the multiple components I had with each other. Since they were all correlated and all needed to update if something in another component updated. The way I fixed this is by having one big parent component that contains all the other (child) components. What I then did is pass a `setState` function to each of them by props, which each component would use to set a refresh function for that component into that state. The parent component then got all the refresh function states from the child components and passed those ones around again to each component so that the components had the ability to refresh another component on  command. This was quite difficult to come up with, but works like a charm.

Another thing that was a little bit tricky was the back-end API. Since I couldn't make the client do the request, because of the API KEYS and fetch CORS. I needed a way to connect my webapp with the Nordigen API. I simply did that by rebuilding the API endpoints I wanted to use from Nordigen with Django on my back-end. That way the clients would send fetch request to the back-end, which would then do the api call and respond to the client with the Nordigen API call response.


## File structure
So within my final project I have two Django apps: `bank_api` and `mony`. The `bank_api` project is the back-end API that recreated the requests made by the front-end to the Nordigen API and respons back accordingly. The `mony` app is the app responsable for the front-end rendering. Within the `templates/mony/` folder `index.html` is the webapp file, `login.html` the login html file, `register.html` the register html file and the `layout.html` file contains the general layout for the other mentioned html files.
Within the `static` file we got `App.js`, which contains the whole React app for the webapp and the `style.css` contains css for the webapp.
Within the `mony` app the `models.py` file contains all models for the app.
The `User` model is standard, however I added a function that it add standard categories to a user's profile if they sign up.
The `Banks` model saves all connected banks. The `Agreements` is a model that holds information about a bank that isn't linked yet. The `Transactions` is a model that holds all transactions of a user. These transactions are also linked with the `Banks` model. The `SpendingCategories` contains all categories linked to a user. With these categories they can assign a transaction to a category

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
