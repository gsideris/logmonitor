# logmonitor
Python GAE project to keep remote information about processes.

This is a project usefull when running time consuming processes and you need regular updates accessible without logging in to netwokrs/vpns.

By logging in to your google account you can access the site [https://logmonitor-163018.appspot.com/](https://logmonitor-163018.appspot.com/) and create a project. At the moment projects are not password protected. You can create any number of 
projects. Each project you create, a uuid is assigned to it, and using that you can post messages to the project without being logged in.


For example I have created a test project 379aa366-ba97-492f-993a-433f9344c7dd that you can see [here - https://logmonitor-163018.appspot.com/project/show?project=379aa366-ba97-492f-993a-433f9344c7dd](https://logmonitor-163018.appspot.com/project/show?project=379aa366-ba97-492f-993a-433f9344c7dd) and you can post messages.

# simple post example
<pre>
curl --data "project=379aa366-ba97-492f-993a-433f9344c7dd&message=test&entry_type=info" https://logmonitor-163018.appspot.com/entry/create
</pre>


# Live Demo
[https://logmonitor-163018.appspot.com/](https://logmonitor-163018.appspot.com/)
