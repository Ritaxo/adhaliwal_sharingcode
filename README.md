Feature: index page
As an authenticated user of the web site
So that  I can see everyone’s posts (problems)
I want to a list of all the posts from the Problem table in the home page index


Feature: dashboard page
As an authenticated user of the web site
So that  I can see my own posts and scripts  
I want to have a page dashboard.html that shows my posts from the Problem table and all my scripts from the Script table

Feature: show_problem, shows one problem from the database
As an authenticated user of the web site
So that  I can read the details of a particular problem  
I want to list all the attributes of a particular problem object (i.e., all fields of one record in the Problem table)

Feature: show_sript, shows the details on one script from the DB
As an authenticated user of the web site
So that  I can read the details and code of a particular python script  
I want to list all the attributes of a particular script object (i.e., all fields of one record in the Script table), the problem that it belongs to and the username of the developer

Feature: edit_problem, edits the users own problem.
As an authenticated user of the web site
I can edit the details and code of the problems that I have posted.  
Once the problem has been posted the user might realize that the wording could have been different or that the problem statement is unclear therefore the user should have the ability to edit their own problem.

Feature: update_problem, updates the problems record in the db.
As an authenticated user of the web site
I can update the details and code of a particular problem  
Once the problem has been posted the user might realize that the wording could have been different or that the problem statement is unclear therefore the user should have the ability to update their own problem.

Feature: delete_problem, deletes the problems record in the db. 
As an authenticated user of the web site
I can delete the details and code of a particular problem  
Once the problem has been posted the user might realize that the problem already exits or that the problem is no longer applicable. Therefore they have the ability to delete their own problem
