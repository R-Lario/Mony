# Mony - Personal Finance Tracking Web Application

Mony is a cool personal finance web app that helps people keep track on their monthly spending. You can connect your European bank accounts with the app, and it'll shows you all your transactions from the last three months. What's really neat is that Mony lets you group your transactions into categories, so you can see where your money's going each month. This app is perfect for anyone who wants to take a closer look at their spending and make smarter money choices.

## Distinctiveness and Complexity
I believe my project is sufficiently distinct from the other projects in this course.

To begin with, my web application is responsive and even for mobiles.

Secondly, this project uses *ReactJS*. React isn't seen in this course and I've decided to learn it to help me build this app. **Why?** Because it is very dynamic. The front end is almost all made with React, so it can interact with API's smoothly. In my opinion React is better suited for this than Vanilla JS. 
If something on the backend changed, the React components will change, therefore changing the front-end. This would seem too much hassle with normal JS, by selecting elements and having to change them. 
Working with React was very challenging, since this was my first project using it and a quite 'difficult' one. For example I had all components connected through the Django REST API. 
This is simply done by fetch requests to the back-end and making the fron-end dynamically change based off the contents of the response.
For example, if a transaction change in the back-end was made it'd be changed and shown immidiatly in the front-end, but also if the user edited a transaction through the front-end, the back-end needed to be updated aswell as all the other components on the front-end. These other components could be grapghs representing information of another component visually.
I've done this, by having 1 big *Master* component with all the individual components as *children*. This Master component links all indiviual children as siblings and makes sure they all update when one of them change. e.g. if a status changes, the graph component changes aswell.

Thirdly, I'm using **Nordigen** 3rd party API to let users connect their European bank account. As mentioned, React works based off these data, but since it wasn't safe to make the API calls from front-end to the 3rd party, I needed to set up my own Django REST API that acts as a *middle man* between the 3rd party bank API and the front-end. 
This middleman sends API requests with the users API token and sends that to the front-end, so the front-end can dynamically make a web page based of the contents. The middle man REST API also stores certain data to its database, like bank account id's, so the transactions from a certain bank account can be accessed any time and you don't have to link it again and again every time.

Also, to make the application more appealing to the user I have decided to implement graphs aswell in the front-end. This was done using the Google graph API. This was also quite challenging, since the documentation wasn't up to date and because of that a simple thing needed a lot of debugging. I made sure the graph kept representing the current data, so if anything changed, the Google graph would change aswell.

To conclude, I think it sufficient, because of the connectivity of everything, the architecture of my web application and all unfamiliar technologies used. 
There are multiple components within my app *- like Google graphs, Django REST Api, React front-end, Nordigen banking API -* that work greatly together that aren't seen in any of the other projects.

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
And now my favorite part, React. Before starting this project I haven't really coded in React, but found it a ton of fun!
Th React file can be found in *mony/static/mony/App.js*. The App has four different *main* components: GoogleDiagrams, TransactionHistory, TransactionCategory, ConnectBank. Each of them serve a different purpose. The main App combines them all together into a working webapp. 

**ConnectBank**: It lets the client connect their bankaccount to the **mony** account.
**TransactionCategory**: Lets the client add/remove categories for their transactions
**TransactionHistory**: This gathers all clients bank transactions and displays them on the site
**GoogleDiagrams**: This makes nice diagrams of the data of the previous components.

There is also some other functions like **accessTokenHandler**, which basically just make sure that the cookies within the clients browser are always good and up-to-date. Within this *App* and it's child components there is a ton of fetch requests going to the back-end to make sure everything gets updated when something changes and everything works. The *React.js App* and *bank_api* go hand in hand in this project.

The most difficult part about this project was learning React.js and connecting all smaller components to work together for sure. I was totally not used to the way React works. What was very difficult is the debugging, making the coding structure and making things efficient within the code.

I hope you guys like my project *mony*
