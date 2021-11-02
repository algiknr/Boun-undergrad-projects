_Project Run_ (READ_ME)

The project was written as a python code. (Python 3.8.1)

I used python standard library imports to achieve this task.

For the first time, It has to be run as (python prep.py) according to where it is located(Desktop in my case).

This run lasts approximately from 30 seconds up to 2 and a half minutes according to the
performance of the computer.This process will do the preprocessing and forming the necessary
json.file along with trie.pickle file. I didn't use a HelperClass.py. So in order to create 
the files(/json/,/pickle/) that we are going to retrieve our information in the next step.
Therefore, you only need to one time run prep.py

You can now erase the reuters21578 because we are not going to need it anymore.

After that, It has to be run as (python query.py) according to where it is located(Desktop in my case).

When you run the code there is going to be "Please enter query key: " prompt after entering the
query string. If you properly give a string it will write out the expected query.However, if you
just directly press enter or just write a "*" without giving any string.It will say "Please don't
forget to enter query key: " prompt until you give a proper key.

There are two types of retriewing query one is single word, the other one is wildcard according
to whether it gets a star(*) at the end or not.

I give the outcome result for each in the report which I obtain from command line terminal.


