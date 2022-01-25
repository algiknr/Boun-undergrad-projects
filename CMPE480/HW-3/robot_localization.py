
#movement probabilities
go=0.8
stay=0.2

#store sensor values relative to wall existence
wallandsensor=[]
#wall true sensor on
wallandsensor.append(0.6)
#wall true sensor off
wallandsensor.append(0.4)
#wall false sensor on
wallandsensor.append(0.1)
#wall false sensor off
wallandsensor.append(0.9)

#take input
array = input ("Enter probability sequence : ")
array=array.split(" ")

inputarray = filter(lambda val: val=="on" or val=="off", array)
inputarray=list(inputarray)
listsize=len(inputarray)

initial=[float(1/3),float(1/3),float(1/3)]

previousprops=[0.0,0.0,0.0]

if listsize==0:
    previousprops=initial

for i in range(int(listsize)) :
    if i==0:
        if inputarray[i]=="off" :
            initial[0]=initial[0]*wallandsensor[3]
            initial[1] = initial[1] * wallandsensor[3]
            initial[2] = initial[2] * wallandsensor[1]
        elif inputarray[i]=="on" :
            initial[0] = initial[0] * wallandsensor[2]
            initial[1] = initial[1] * wallandsensor[2]
            initial[2] = initial[2] * wallandsensor[0]

        total=0
        total=initial[0]+initial[1]+initial[2]

        #normalization
        initial[0]=initial[0]/total
        initial[1] = initial[1] /total
        initial[2] = initial[2] / total

        if not listsize==1:
            # first is stay at 0 (index)
            previousprops[0]=stay*initial[0]

            # second is whether move 1 from 0 or stay at 1
            previousprops[1]=go*initial[0]+stay*initial[1]

            # third is whether move 2 from 1 or stay at 2
            previousprops[2] = go * initial[1] + 1 * initial[2]
        else:
            previousprops[0]=initial[0]
            previousprops[1] = initial[1]
            previousprops[2] = initial[2]
    else:
        temp_previousprops=[0.0,0.0,0.0]

        if inputarray[i] == "off":
            previousprops[0] = previousprops[0] * wallandsensor[3]
            previousprops[1] = previousprops[1] * wallandsensor[3]
            previousprops[2] = previousprops[2] * wallandsensor[1]
        elif inputarray[i]== "on":
            previousprops[0] = previousprops[0] * wallandsensor[2]
            previousprops[1] = previousprops[1] * wallandsensor[2]
            previousprops[2] = previousprops[2] * wallandsensor[0]

        total = 0
        total = previousprops[0] + previousprops[1] + previousprops[2]

        # normalization
        previousprops[0] =  previousprops[0] / total
        previousprops[1] =  previousprops[1] / total
        previousprops[2] =  previousprops[2] / total

        if not i==len(inputarray)-1:
            # first is stay at 0 (index)
            temp_previousprops[0] = stay *  previousprops[0]

            # second is whether move 1 from 0 or stay at 1
            temp_previousprops[1] = go *  previousprops[0] + stay * previousprops[1]

            # third is whether move 2 from 1 or stay at 2
            temp_previousprops[2] = go *  previousprops[1] + 1.0 * previousprops[2]

            previousprops[0]=temp_previousprops[0]
            previousprops[1]=temp_previousprops[1]
            previousprops[2]=temp_previousprops[2]


print(previousprops)
