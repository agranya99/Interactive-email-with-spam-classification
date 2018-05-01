#Code snippet to order e-mails by receiving date and time
import re
from datetime import datetime
from datetime import time

datetime_object1 = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
print(datetime_object1)
f=open('Untitled Document', 'r')
f_contents=f.read()
#print(f_contents)
#datetime_object = datetime.strptime(f_contents, '%b %d, %Y at %I:%M%p')
def getdate(f_contents):
	dateobj=re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d\d,\s+\d\d\d\d", f_contents)
	timeobj=re.search("\d{1,2}:\d\d\s+[PA]M", f_contents)
	if dateobj and timeobj:
		date=dateobj.group(0)
		date=''.join(e for e in date if (e.isalnum() or e.isspace()))
		time=timeobj.group(0)
		time=''.join(e for e in time if (e.isalnum() or e==':'))
		date_time=date+" "+ time
		datetime_object = datetime.strptime(date_time, '%b %d %Y %I:%M%p')
		return datetime_object
#print(date)

class Stack:
     def __init__(self):
         self.items = []
     def isEmpty(self):
         return self.items == []
     def pushT(self, item):
         self.items.append(item)
     def push(self, item):
         temp=Stack()
	 if self.isEmpty() or getdate(item)>getdate(self.peek()):
	 	self.pushT(item)
	 else:
	 	while getdate(item)<getdate(self.peek()):
	 		temp.pushT(self.pop())
	 	self.pushT(item)
	 	while not(temp.isEmpty()):
	 		self.pushT(temp.pop())
     def pop(self):
         return self.items.pop()
     def peek(self):
         return self.items[len(self.items)-1]
     def size(self):
         return len(self.items)
spam_stack=Stack()
ham_stack=Stack()
