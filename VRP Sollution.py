import time
import random
import copy
from graphics import *
from geopy import distance




def loadData():
    file = open("dane.txt", "r", encoding="UTF-8")
    data = file.readlines()

    for i in range(len(data)):
        data[i] = data[i].split()


    
    return data


def roadLength(x,y):
    #a = abs( x[0] - y[0] )
    #b = abs( x[1] - y[1] ) 
    #return round(math.sqrt( a**2 + b**2 ), 3)
    dis = round(distance.distance(x,y).km, 3)
    return dis

def findRoute(data, trucks, capacity):

    startPoint = data[1] 

    locations = data[2:]

    routes = []
    for i in range(trucks):
        routes.append( [[startPoint[1], 0, capacity, startPoint[3], startPoint[4]]] )


    while len(locations) > 0:
        newcity = locations.pop(random.randint(0,len(locations)-1))
        truckNumber = random.randint(0,trucks-1)

        oldcity = routes[truckNumber][-1]

        road = roadLength([float(oldcity[3]),float(oldcity[4])],[float(newcity[3]),float(newcity[4])])
        newcapacity = int(oldcity[2]) - int(newcity[2])
        newroad = round(oldcity[1] + road,3)

        if newcapacity >= 0:
            routes[truckNumber].append([newcity[1],newroad,newcapacity,newcity[3],newcity[4]])
        else:
            locations.append(newcity)
            
            error = 0
            for i in routes:
                if int(i[-1][2]) >= int(newcity[2]):
                    pass
                else:
                    error += 1    
            if error == trucks:
                return "ERROR"

    for i in routes:
        road = roadLength([float(i[-1][3]),float(i[-1][4])],[float(startPoint[3]),float(startPoint[4])])
        newroad = round(i[-1][1] + road,3)
        i.append( [startPoint[1], newroad, i[-1][2], startPoint[3], startPoint[4]] )


    
    return routes


def isPresent(routes,cityname):
    for i in routes:
        if i[0] == cityname:
            return True
    return False


def mixRoutes(rou1,rou2, mixpoint):

    r1 = copy.deepcopy(rou1)
    r2 = copy.deepcopy(rou2)
    
    max = len(r1)

    r1cut = r1[mixpoint]
    r2cut = r2[mixpoint]

    newr1 = []
    newr2 = []


    for i in r1:
        for j in range(len(i)-1,0,-1):
            i[j][2] = i[j-1][2] - i[j][2] 
            i[j][1] = 0

    for i in r2:
        for j in range(len(i)-1,0,-1):
            i[j][2] = i[j-1][2] - i[j][2] 
            i[j][1] = 0


    indexroute1 = len(r1cut)
    indexroute2 = len(r2cut)

    for i in range(max):
        if i == mixpoint:
            route1 = []
            route2 = []

            for j in r2cut:
                route1.append(j)
            for j in r1cut:
                route2.append(j)


            newr1.append(route1)
            newr2.append(route2)
        else:
            route1 = [r1[0][0]]
            route2 = [r2[0][0]]
            
            for j in r1[i]:
                if isPresent(r2cut,j[0]):
                    pass
                else:
                    route1.append(j)

            for j in r2[i]:
                if isPresent(r1cut,j[0]):
                    pass
                else:
                    route2.append(j)
            
            route1.append([r1[0][-1][0], 0, 0,r1[0][-1][3],r1[0][-1][4]])
            route2.append([r2[0][-1][0], 0, 0,r2[0][-1][3],r2[0][-1][4]])

            newr1.append(route1)
            newr2.append(route2)


    leftoversr1 = []
    leftoversr2 = []

    for j in r1cut:
        if isPresent(r2cut,j[0]):
            pass
        else:
            leftoversr1.append(j)

    for j in r2cut:
        if isPresent(r1cut,j[0]):
            pass
        else:
            leftoversr2.append(j)


    capacityleftr1 = []
    for i in range(len(newr1)):
        capacityleftr1.append(newr1[0][0][2])
    
    capacityleftr2 = []
    for i in range(len(newr2)):
        capacityleftr2.append(newr2[0][0][2])


    for i in range(len(newr1)):
        for j in newr1[i][1:]:
            capacityleftr1[i] -= j[2]


    for i in range(len(newr2)):
        for j in newr2[i][1:]:
            capacityleftr2[i] -= j[2]



    leftoversr1.sort(reverse = True,key = lambda leftoversr1: leftoversr1[2])
    leftoversr2.sort(reverse = True,key = lambda leftoversr2: leftoversr2[2])



    while len(leftoversr1) > 0:
        
        city = leftoversr1.pop(0)
        city = copy.deepcopy(city)
        for i in range(len(capacityleftr1)):
            if city[2] < capacityleftr1[i]:
                newr1[i].insert(-1,city)
                capacityleftr1[i] -= city[2]
                break
        
    while len(leftoversr2) > 0:
        
        city = leftoversr2.pop(0)
        city = copy.deepcopy(city)
        for i in range(len(capacityleftr2)):
            if city[2] < capacityleftr2[i]:
                newr2[i].insert(-1,city)
                capacityleftr2[i] -= city[2]
                break

                
    for i in newr1:
        for j in range(1,len(i)):
            capacity = i[j-1][2] - i[j][2]
            i[j][2] = capacity
            
            road = roadLength([float(i[j-1][3]),float(i[j-1][4])],[float(i[j][3]),float(i[j][4])])
            newroad = round(i[j-1][1] + road,3)
            i[j][1] = newroad

    for i in newr2:
        for j in range(1,len(i)):
            capacity = i[j-1][2] - i[j][2]
            i[j][2] = capacity

            road = roadLength([float(i[j-1][3]),float(i[j-1][4])],[float(i[j][3]),float(i[j][4])])
            newroad = round(i[j-1][1] + road,3)
            i[j][1] = newroad


            
    return [newr1,newr2]



def mutation(r):
    route = copy.deepcopy(r)

    error = 0
    for i in route:
        if len(i) < 4:
            error +=1
    if error == len(route):
        return "ERROR"

    randomcar = random.randint(0,len(route)-1)
    while len(route[randomcar]) < 4:
        randomcar = random.randint(0,len(route)-1)

    a = random.randint(1,len(route[randomcar])-2)
    b = random.randint(1,len(route[randomcar])-2)
    while a == b:
        b = random.randint(1,len(route[randomcar])-2)
    
    for i in route:
        for j in range(len(i)-1,0,-1):
            i[j][2] = i[j-1][2] - i[j][2] 
            i[j][1] = 0

    citya = route[randomcar][a]
    cityb = route[randomcar][b]

    route[randomcar][a] = cityb
    route[randomcar][b] = citya

    for i in route:
        for j in range(1,len(i)):
            capacity = i[j-1][2] - i[j][2]
            i[j][2] = capacity

            road = roadLength([float(i[j-1][3]),float(i[j-1][4])],[float(i[j][3]),float(i[j][4])])
            newroad = round(i[j-1][1] + road,3)
            i[j][1] = newroad
    
    return route



def findRoutes(number, trucks, capacity):
    data = loadData()

    allroutes = []
    for i in range(number):
        routes = "ERROR"
        errors = -1
        while routes == "ERROR":
            routes = findRoute(data, trucks, capacity)
            errors +=1
        allroutes.append(routes)
    return allroutes



def routeInfo(route):
    roads = []
    capacity = []
    sumroads = 0
    sumcapacity = 0
    sumcity = 0

    for i in route:
        for j in i:
            sumcity += 1

    for i in route:
        roads.append(i[-1][1])
        capacity.append(i[-1][2])
        sumroads += i[-1][1]
        sumcapacity += i[-1][2]

    return [round(sumroads,3), roads, capacity, sumcapacity, sumcity]



def geneticAlgorythm(population, trucks, capacity, generations, crosses, mutations):

    save = []

    allroutes = findRoutes(population, trucks, capacity)
    print("\npopulation:", len(allroutes), " trucks:", trucks, " capacity:", capacity)
    
    for i in allroutes:
        print(routeInfo(i))
    print("\n")

    currentgeneration = generations
    while currentgeneration > 0:

        
        currentcrosses = crosses
        while currentcrosses > 0:

            correct = 0
            while correct == 0:
                r1 = random.randint(0,population-1)
                r2 = random.randint(0,population-1)
                
                while r1 == r2:
                    r2 = random.randint(0,population-1)

                randomcar = random.randint(0,trucks-1)

                newroutes = mixRoutes(allroutes[r1],allroutes[r2],randomcar)

                info1 = routeInfo(newroutes[0])
                info2 = routeInfo(newroutes[1])

                citynumber = routeInfo(allroutes[0])[-1]
                

                if info1[-1] == info2[-1] and info1[-1] == citynumber:
                    correct = 1
                
                if correct == 1:
                    for i in range(trucks):
                        if info1[1][i] == 0.0 or info2[1][i] == 0.0 or info1[2][i] < 0 or info2[2][i] < 0 or info1[2][i] > capacity or info2[2][i] > capacity:
                            correct = 0


            allroutes.append(newroutes[0])
            allroutes.append(newroutes[1])

            currentcrosses -= 1

        
        currentmutations = mutations
        while currentmutations > 0:

            randomroute = random.randint(0,len(allroutes)-1)
            mutatedroute = mutation(allroutes[randomroute])
            while mutatedroute == "ERROR":
                randomroute = random.randint(0,len(allroutes)-1)
                mutatedroute = mutation(allroutes[randomroute])

            allroutes[randomroute] = mutatedroute

            currentmutations -= 1


        allroutessorted = []
        for i in allroutes:
            allroutessorted.append([i,routeInfo(i)])

        allroutessorted.sort(key = lambda allroutessorted: allroutessorted[1][0])
        
        
        allroutes = []
        for i in range(population):
            allroutes.append(allroutessorted[i][0])


        if (currentgeneration-1)%10 == 0:
            print("gen:",generations-currentgeneration+1, )
            info = routeInfo(allroutes[0])
            print("DISTANCES:",info[1],"   TOTAL =", info[0], "km")
            print("CARGO LEFT:",info[2],"   TOTAL =",info[3],"\n")

        save.append(allroutes[0])
        

        currentgeneration -= 1

    print("\nNEW")

    for i in allroutes:
        print(routeInfo(i))
    

    print("\nBEST SOLLUTION")
    info = routeInfo(allroutes[0])
    print("DISTANCES:",info[1],"   TOTAL =", info[0], "km")
    print("CARGO LEFT:",info[2],"   TOTAL =",info[3],"\n")

    for i in allroutes[0]:
        abc = []
        print("ROUTE")
        for j in i:
            abc.append(j[0])
        print(abc)

    print("\nCOMPLETE ROUTE")
    for i in allroutes[0]:
        print(i)


    return save


def graph(d,wx,wy):

    data = d[-1]
    x = []
    y = []
    for i in data:
        x.append([])
        y.append([])

    for i in range(len(data)):
        for j in data[i]:
            x[i].append(round( (float(j[4])*120)-1700, 0))
            y[i].append(round( (6600-float(j[3])*120), 0))


    win = GraphWin('Best Sollution', wx, wy, autoflush=False)
    win.setCoords(0,750,1150,0)
    colours = ["red","green","blue","yellow","lightblue","lightgreen","purple", "cyan", "gray", "pink"]

    for i in range(len(data)):
        for j in range(len(data[i])-1):
            l = Line(Point(x[i][j],y[i][j]), Point(x[i][j+1],y[i][j+1])) 
            l.setWidth(3)
            l.setFill(colours[i])
            l.draw(win)

            c = Circle(Point(x[i][j],y[i][j]), 5)
            c.setFill(colours[i])
            c.setOutline(colours[i])
            c.draw(win)
    
    for i in range(len(data)):
        for j in range(len(data[i])-1):
            name = Text(Point(x[i][j],y[i][j]-10), data[i][j][0])
            name.setSize(10)
            name.setStyle("bold") 
            name.draw(win)
    
    win.getMouse()
    win.close()


def graphSlides(d,wx,wy):

    win2 = GraphWin('Best of generations', wx, wy, autoflush=False)
    win2.setCoords(0,750,1150,0)
    colours = ["red","green","blue","yellow","lightblue","lightgreen","purple", "cyan", "gray", "pink"]

    while True:
        for index in range(len(d)):
            data = d[index]
            x = []
            y = []

            road = routeInfo(data)[0]

            for i in data:
                x.append([])
                y.append([])

            for i in range(len(data)):
                for j in data[i]:
                    x[i].append(round( (float(j[4])*120)-1700, 0))
                    y[i].append(round( (6650-float(j[3])*120), 0))

            for item in win2.items[:]:
                item.undraw()
            

            for i in range(len(data)):
                for j in range(len(data[i])-1):
                    l = Line(Point(x[i][j],y[i][j]), Point(x[i][j+1],y[i][j+1])) 
                    l.setWidth(3)
                    l.setFill(colours[i])
                    l.draw(win2)

                    c = Circle(Point(x[i][j],y[i][j]), 5)
                    c.setFill(colours[i])
                    c.setOutline(colours[i])
                    c.draw(win2)
            
            for i in range(len(data)):
                for j in range(len(data[i])-1):
                    name = Text(Point(x[i][j],y[i][j]-10), data[i][j][0])
                    name.setSize(10)
                    name.setStyle("bold") 
                    name.draw(win2)
            
            t = "GENERATION: " + str((index+1)) + "   TOTAL DISTANCE: " + str(road) + " KM"
            text = Text(Point(1150/2,20), t)
            text.setSize(10)
            text.setStyle("bold")
            text.draw(win2)

            win2.update()
            time.sleep(0.1)
        time.sleep(5)





trucks = 5
capacity = 1000

population = 100
generations = 250
crosses = 10
mutations = 5

windowx = 1024
windowy = 768

t1 = time.time()
best = geneticAlgorythm(population,trucks,capacity,generations,crosses,mutations)
t2 = time.time()
print("\nTIME:",round(t2-t1,3), "s")

graph(best,windowx,windowy)
graphSlides(best,windowx,windowy)
