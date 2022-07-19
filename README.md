# Innotter
Innowise Internship task


This is an API whose logic is similar to twitter/reddit. There are three roles: administrator, moderator, user. The administrator has the right to view any pages, block them for any period of time and permanently, delete any posts and block users. The moderator has the right to view any pages, block them for any period of time, delete any posts. The user can register, log in. Authentication is carried out using the jwt token. After the authentication process, the user can create a page and write posts on it, subscribe to other pages, in the case of a blocked page, send a subscription request, put likes. The project also has a microservice that calculates statistics for each page.
