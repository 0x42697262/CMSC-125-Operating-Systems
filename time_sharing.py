# CS125 - Machine Problem 1
import random
import time
import os
from datetime import datetime, timedelta

class User:
    def __init__(self, name, resources = []):
        self.name = name;
        self.resources = resources;
    def __repr__(self):
        return self.name
    def allResources(self):
        return str(self.resources) + '\n'
    
class UserResource:
    def __init__(self, name, duration):
        self.name = name;
        self.duration = duration;
    def __repr__(self):
        return str(self.name)

    
class Resource(UserResource):
    def __init__(self, name, idle, users = []):
        self.name = name;
        self.idle = idle
        self.users = users;
    def __repr__(self):
        return str(self.name)
    def showUsers(self):
        return str(self.name) + ' : ' + str(self.users)

class Time:
    def __init__(self, tick):
        self.tick = tick;
    def __repr__(self):
        return str(self.tick)

def generateNumber(x):
    return random.randint(1,x)

def generateNonRandom(x):
    num = list(range(1,x))
    random.shuffle(num)
    return num

# Generate a random number of resources (1-30). Label them by resource number, between 1 - 30.
# Generate a random number of users (1-30). Label them by user number between, 1-30.
# Generate the random resource that a user will need and the length of the time that the user will use the resource (1-30 seconds). The resource(s) that a user will request must only be those randomly generated resources (from #1).

k = 10
resources = generateNumber(k)
users = generateNumber(k)
user_list = []
resource_list = []
duration_list = []
totalTime = []
# The queue for all resources
resource_queue = []

def createResources():
    for i in range(resources):
        newResource = Resource('R' + repr(i + 1), 0, [])

        for user in user_list:
             if user.resources[0].name == newResource.name:
                 newResource.users.append(user)
        resource_list.append(newResource)
    # print(resource_list)

def createUsers():
    print("\n\t\t\t»»————-　★　————-««")
    print("\n\t\t       <<Allocating Resources>>")
    print("\n\t\t\t»»————-　★　————-««")
    for i in range(users):           
        newUser = User('U' + repr(i + 1), [])
        res_for_users = generateNumber(resources)
        print(str(newUser.name) + ' : ' + repr(res_for_users) + ' resources')

        temp = generateNonRandom(res_for_users + 1)
        for i in range(res_for_users):
            # Prevents users from using duplicate resources
            duration = generateNumber(k)
            newResource = UserResource('R' + repr(temp[i]), duration)

            duration_list.append(newResource.duration)
            totalTime.append("{} = {}".format(newResource.name,newResource.duration))
            resource_queue.append(newResource.name)
            newUser.resources.append(newResource)
        # print(newUser.allResources())
        user_list.append(newUser)
    # print(totalTime)
    time.sleep(1)


# The program should be able to display the status of the resources, including the user currently using the resource, the time (or time left) that the user needs to use the resource.
# The program should also be able to list the users “in waiting” of a resource, if there are any, and when these users will be able to start using the resource.
# Finally, the program should be able to say when the resources will be free of users (meaning, no user needs to use the resource).


def createUserTable():
    print("\n\t\t\t»»————-　★　————-««")
    print("\t\t\t   <<User Table>>")
    print("\t\t\t»»————-　★　————-««\n")
    for user in user_list:
        print("User: " + str(user.name))
        print("Assigned Resources: " + str(user.allResources()))

def createResourceTable():
    print("\n\t\t\t»»————-　★　————-««")
    print("\t\t\t <<Resource Table>>")
    print("\t\t\t»»————-　★　————-««\n")
    for res in resource_list:

        q = resource_queue.count(str(res)) - 1

        if len(res.users) > 0:

            print("...")
            print("Resource: " + str(res.name))
            print("User: " + str(res.users[0]))
            print("Time remaining: " + str(res.users[0].resources[0].duration) + " seconds")

            try:
                print("User in Waiting for Immediate use: " + str(res.users[1]) + " (" + str(res.users[0].resources[0].duration) + ") ")
                print("Queue: " + str(q) + " users in queue") 
                # print("Free in: " + str(res.idle) + " seconds")
                print("...")
                print("\n")
            except IndexError:
                print("User in Waiting for Immediate use: None")
                print("Queue: " + str(q) + " users in queue") 
                # print("Free in: " + str(res.idle) + " seconds")
                print("\n")


def totalDuration(t):
    print("\nTotal Duration: " + str(t))

def no_users():
    for res in resource_list:
        # Records when the resources will be free of users
        # if len(res.users) > 0:
        i = len(totalTime)
        for j in range(i):
            l = totalTime[j]
            if res.name == l[0:2] or l[0:3]:
                res.idle += int(l[-1])



def simulate():
    done = False
    t = Time(timedelta(minutes = sum(duration_list)/60, seconds = sum(duration_list)%60))
    while (done == False):

        time.sleep(0.3)
        os.system("cls")
        createUserTable()
        createResourceTable()
        # totalDuration(t)

        done = True
        for res in resource_list:
            if len(res.users) > 0: #Check if there are users lined up for the resource
                res.users[0].resources[0].duration -= 1
                res.idle -= 1
                t.tick -= timedelta(seconds = 1)

                if res.users[0].resources[0].duration < 0: #Check if time is up for that specified resource
                    # print(res.users[0].resources)
                    res.users[0].resources.remove(res.users[0].resources[0])
                    resource_queue.remove(str(res.name))

                    if len(res.users[0].resources) > 0: #Check if there are other resources in line for the user and then assign that user to that resource
                        next = res.users[0].resources[0].name
                        next_ = int(next[1:]) - 1
                        resource_list[next_].users.append(res.users[0])

                    res.users.remove(res.users[0]) # Remove user for that resource
                done = False

    os.system("cls")
    print("\t    »»————-　★　————-««")
    print("\tSystem has finished all tasks!")
    print("\t    »»————-　★　————-««")
    # print(r"""\______________$$$$$$$$$$____________________
    # _____________$$__$_____$$$$$________________
    # _____________$$_$$__$$____$$$$$$$$__________
    # ____________$$_$$__$$$$$________$$$_________
    # ___________$$_$$__$$__$$_$$$__$$__$$________
    # ___________$$_$$__$__$$__$$$$$$$$__$$_______
    # ____________$$$$$_$$_$$$_$$$$$$$$_$$$_______
    # _____________$$$$$$$$$$$$$_$$___$_$$$$______
    # ________________$$_$$$______$$$$$_$$$$______
    # _________________$$$$_______$$$$$___$$$_____
    # ___________________________$$_$$____$$$$____
    # ___________________________$$_$$____$$$$$___
    # __________________________$$$$$_____$$$$$$__
    # _________________________$__$$_______$$$$$__
    # ________________________$$$_$$________$$$$$_
    # ________________________$$$___________$$$$$_
    # _________________$$$$___$$____________$$$$$$
    # __$$$$$$$$____$$$$$$$$$$_$____________$$$_$$
    # _$$$$$$$$$$$$$$$______$$$$$$$___$$____$$_$$$
    # $$________$$$$__________$_$$$___$$$_____$$$$
    # $$______$$$_____________$$$$$$$$$$$$$$$$$_$$
    # $$______$$_______________$$_$$$$$$$$$$$$$$$_
    # $$_____$_$$$$$__________$$$_$$$$$$$$$$$$$$$_
    # $$___$$$__$$$$$$$$$$$$$$$$$__$$$$$$$$$$$$$__
    # $$_$$$$_____$$$$$$$$$$$$________$$$$$$__$___
    # $$$$$$$$$$$$$$_________$$$$$______$$$$$$$___
    # $$$$_$$$$$______________$$$$$$$$$$$$$$$$____
    # $$__$$$$_____$$___________$$$$$$$$$$$$$_____
    # $$_$$$$$$$$$$$$____________$$$$$$$$$$_______
    # $$_$$$$$$$hg$$$____$$$$$$$$__$$$____________
    # $$$$__$$$$$$$$$$$$$$$$$$$$$$$$______________
    # $$_________$$$$$$$$$$$$$$$__________________
    # """)

createUsers()
createResources()
no_users()
simulate()