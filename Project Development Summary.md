# Project Summary

I hope you’ve enjoyed my Finch demo app! 

When I first sat down to work on this app, my brain went many different directions on how to approach it. To settle my brain and get the ball rolling, I decided to focus on the core functions of the app: 
- creating a connection with Finch
- pulling data from the Finch API using my access token—starting with the directory data. 

Once these functions were defined and tested, the next step was to create the interface the end user would interact with to create a connection. I built out a form using the parameters set out in the project sheet, and ran into my first big issue: where should I store the access token? 

I didn’t want to create a whole database for the app, but also wanted something at least somewhat secure. For the sake of speeding development, I  simply put the access token into the Flask session object, which stores session data in a cookie on the browser encrypted by an application secret key. That worked at first, but would cause some issues down the line. 

Now I had a basic form that created a connection, and could see the directory information dumped out on the `/directory` endpoint. The next step was formatting the data and making it look nice. I created a simple, clean table to present the data, and iterated over the json keys to output the contents. Where the contents included a sub-dictionary, I created a sub table. I also created a basic dropdown-like experience so users could click on individual names to reveal the employee details.  I also implemented a similar interface for the employment and company info pages. 

For a complete user experience, I needed a way to close out the connection as well as open it. Unfortunately this wasn’t easy from the server side, since my session data was held on the client in a cookie. Looking online for help, the only advice I found on clearing secure cookie data was to change the application secret key, which isn’t really a practical solution for a web app. So I decided to store the access token and session info server-side using Redis, a more secure method in general as long as the Redis server is secured. 

Now I had a clean user experience that allowed the user to start a new session with a single Finch connection, view all the relevant data they need, then close out their session when they are done. With all that done, I went back over my app and tested various providers, ensuring that I had rudimentary error handling in place so the app doesn’t crash when it receives upstream errors or data is formatted in an unexpected way. I am sure I didn’t catch everything, but the basic errors should be covered. 

This was a wonderful exercise and I learned a lot creating the application. Given more time, I’d love to try my hand at building the app out with Finch’s production API and the native Python Finch client, rather than calling the sandbox url directly. I’d also strengthen the nuts and bolts of the application by building out a more robust testing and error handling suite, and making sure my access token is encrypted and secure on my Redis server. 

I have a couple quick questions for the Finch team that came up during this project:
- I noticed that the endpoints I used do not have an equivalent call in the Finch python client. For instance,  `/api/employer/directory` has `client.hris.directory.list()` in production, but the sandbox only has the `update()` method implemented, and not `client.sandbox.list()`. Is this something the Finch team is implementing in the future, or is it left out for a reason? Or did I simply miss where it might be?
- How does Finch store access tokens on their end? 
