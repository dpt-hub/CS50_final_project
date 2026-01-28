# Client Route Optimization Web App (CS50x Final Project)

![Main screen of a route optimization app, showing a map](/Images/RapidRep.png)

## TL;DR

RapidRep is a route management tool designed for field salespeople to visualize and track client visits. While the goal was to implement automated route optimization, the current version focuses on the bases to accomplish that task: client mapping, visit reporting, and simple perfomance analytics.

Developed over 68 hours as a CS50x Final Project, I initially challenged myself to use only official language/framework documentation (meaning no StackOverflow, Reddit, ...) but I started regretting that decision as I began to realize that my learning progress was at stake (you learn alot by reading how people explain problems in different ways). Besides helping me with marketing copy, I didn't use LLM's for coding purposes.

#### Video: [https://youtu.be/lmFS3ih4i1s]

## Context Behind The Project

Let me start by saying that my goal with this project was to learn. I took CS50x with a very specific path in mind. I found a problem in how field salespeople in Portugal plan their days and this insight made me want solve this problem. I quickly understood that, to solve this, I would need some kind of algorithm or tech to help. 

This realization meant that I would have to: 
1) Convince my cofounder to enroll another person, find someone whom we could trust and could deliver, sell them our vision and depend on their work.
2) Move on with another, "simpler" idea.
3) Learn to program.

I choose the later.

> "What ultimately matters in this course is not so much where you end up relative to your classmates but where you end up relative to yourself when you began."

Before enroling in CS50x I took some freeCodeCamp courses on Javascript. The tutorials made coding look easy with simple `if` statements, `for` loops and easy-to-understand functions. I felt like a genius. But when I started to bit off more than I could chew, and looked at real-world projects, I felt lost again. It felt as if I had been taught basic addition, only to be dropped into the middle of an algebra exam and told to "find x".

This course fundamentally changed how I see programming. It taught me that being confused is part of the process. You will start off by not understanding how most things work, and it's fine! CS50x excels at making you comfortable with being uncomfortable. By actually trying to solve problems on my own without a hand-held walkthrought of another "beginner-friendly" tutorial, I was forced to figure it out. And that is where I felt the real learning happened.

Now to the project itself.

## Features

### Back-end

I built the back-end using Python and the Flask framework. For data storage, I went with SQLite because I wanted a relational database that was lightweight and that I already knew how to use. I used the sqlite3 library to manage these data connections and the os library to handle the environment, specifically to ensure the app's instance folder and database file were created and located correctly on the server. To keep the app secure, I used Werkzeug for password hashing.

### Front-end

On the front-end, I used HTML to build the structural foundation of the app, ensuring every view was organized and semantic. To handle the logic of the UI and the communication with the server, I used JavaScript. The mapping was done via Leaflet.js, which allowed me to transform database coordinates into a dynamic map, while Chart.js was integrated to turn raw numbers into clean, readable graphs. Everything is wrapped in Bootstrap, which gave me pre-built components so I could focus on the functionality of the map rather than reinventing the wheel with custom CSS.

### App in Action

I wanted the first impression to be clear and the barrier to entry low. The landing page explains the core value of the project immediately.

![Homepage of RapidRep](/Images/Landing_page.png)

Before even signing up, I built an ROI Calculator to give business owners a concrete reason to care about optimizing their routes.

![ROI Calculator](/Images/ROI_calculator.png)

I created a secure authentication system so that multiple users can use the platform. Each salesperson has their own private workspace, ensuring that client lists and revenue data stay personal and protected.

![Register page of RapidRep](/Images/Register.png)

I also made sure to include clear error handling, such as alerts for incorrect login details, to make the experience feel reliable.

![Login page of RapidRep with an error alert on top](/Images/Login_error.png)

The Map View is the heart of the project. It takes your entire client list and plots them as interactive markers so you can see your sales territory at a glance.

![Main screen of RapidRep's app, showing markers on the map](/Images/Map_markers.png)

You can add new clients directly through the map, which makes it much easier to visualize gaps in your current coverage as you navigate.

![Main screen of RapidRep's app, showing adding a client on the map](/Images/Map_add_client.png)

Clicking a marker gives you instant access to that specific client's details without having to leave the geographic view.

![Main screen of RapidRep's app, showing a pressed marker on the map](/Images/Map_check_client.png)

I wanted to make the "boring" part of the job—data entry—as efficient as possible. The main list view allows for full control to add, edit, or delete client information as your business grows.

![Clients screen of RapidRep's app, showing a list of clients on a table](/Images/Client_list.png)

The interface includes dedicated forms for adding new contacts to the database.

![Clients screen of RapidRep's app, showing the add client feature](/Images/Client_list_add.png)

It also handles updates, so you can keep client details accurate over time.

![Clients screen of RapidRep's app, showing the edit client feature](/Images/Client_list_edit.png)

I added a multi-select and bulk delete feature to help users manage large datasets quickly without the frustration of deleting entries one by one.

![Clients screen of RapidRep's app, showing the multi-select clients](/Images/Client_list_select.png)

Confirming deletions helps prevent accidental data loss while keeping the workspace clean.

![Clients screen of RapidRep's app, showing delete client feature](/Images/Client_list_delete.png)

The system is designed to handle empty states, prompting the user when it’s time to start adding data.

![Clients screen of RapidRep's app, showing the list empty](/Images/Client_list_empty.png)

I built a reporting system that connects daily visits to revenue. Using Chart.js, the app generates monthly reports so you can see your performance trends at a glance.

![Reports screen of RapidRep's app, showing two graphs and a table of visits](/Images/Visits_report.png)

The process of logging a visit is integrated directly into the reports page to keep the workflow simple.

![Reports screen of RapidRep's app, showing the add visit feature](/Images/Visits_report_add.png)

Even when you're just starting out, the layout stays organized and ready for your first entries.

![Reports screen of RapidRep's app, showing the report empty](/Images/Visits_report_empty.png)

## Self Constraint

To push myself, I started this project with a self-imposed rule: use only official documentation. However, as I got deeper into it, I made the conscious choice to pivot. The turning point came when I looked at a past exercise from Harvard's Flask documentation and realized it was far more accessible than the official language specs. It explained the concepts in a way that actually clicked, and I decided then that my goal should be understanding the logic, not just struggling through a manual for the sake of it.

I brought Stack Overflow and other search forums back into my workflow to help bridge those gaps, but I stayed away from AI tools entirely. I wanted to make sure that even if I was looking for help, I was still the one doing the thinking and writing the code.

## What’s Missing

I’m really proud of how far this project has come, but as I look at it, there are a lot of things that need fixing to be complete. Here's a non-comprehensive list:

### Things that bug me about the design

- Right now, the map height is fixed in pixels, so it looks a bit weird when you change the window size.

- There is no mobile responsiveness so it's strictly a desktop experience.

- The UI feels a bit bland. 

- Once you add a lot of data, the tables just keep growing down the page.

### What’s missing for the user

- Adding a client through the list view is currently a bit of a chore because you have to manually input latitude and longitude.

- You can't filter, select, or change settings directly on the Map section yet.

- Even though the goal is route optimization, the map doesn't show actual routes or paths between clients.

- There’s no CSV uploader, so you have to enter every client by hand.

- The reports are fixed. I wanted to make them customizable so users can pick what data they want to see.

- If the user deletes a client, the visits of that client aren't deleted. This means that when the user creates another client those "dead" visits go to the client created.

### What I need to clean up in the code

- I didn’t stick to DRY. I copy-pasted a lot of code across main.py, JS, and HTML just to get things working.

- The tables use a Bubble Sort algorithm I wrote for the front-end. It works for a few clients, but it’ll get slow once the database grows.

- Instead of using Sass properly, I just overrode things in styles.css, which makes it look a little "off."


I could go on and on about what is missing and what should be improved, but for a 68-hour sprint starting from an empty file, I’m happy with where I'm at. RapidRep isn't a finished product, and it hasn't solved the routing problem yet. But it is the working proof that I can build the foundation needed to get me there. It’s no longer just an idea, and that's what matters to me.
