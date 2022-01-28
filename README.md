# AbstractAlgebraFun
This is my implementation of abstract algebra concepts (on groups). This repo includes two files where one represents a standard group (Group.py) and a file that contains some group functions (GroupFunctions.py). To help with special groups, I have added D3 and D4.

I also implemented a nice method for determining or defining a group rule from a Cayley Table.

There are examples of how to utilize these functions in the GroupFunctions.py file. 

For example, you can make the group of integers module 3 by defining a group like:
```
# defines a group with the domain, the rule, and (optinally) the identity.
z_3 = Group(g=list(range(3)), rule="({0}+{1})%3", e=0)
```
