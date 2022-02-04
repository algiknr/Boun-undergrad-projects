import datetime
import math
from numpy import random
import numpy as np
def Example(List):
    y=0;
    n=len(List);
    for i in range(n):
        if List[i]==0:
            for j in range(i,n,1):
                c = int(math.log2(n));
                for k in range(0,c+1,1):
                    y=y+1;
        else:
            for m in range(i,n,1):
                for t in range(1,n+1,1):
                    x=n;
                    while x>0:
                        x=x-t;
                        y=y+1;
    return y;


if __name__ == '__main__':
    inputSizes = np.array([1, 10, 50, 100, 200, 300, 400, 500, 600, 700]);

    for i in range(10):
        s=inputSizes[i];
        randomList2= random.randint(2, size=(s, 1));
        bestList=np.zeros((s,), dtype=int);
        worstList = np.ones((s,), dtype=int);

        start_time = datetime.datetime.now()
        Example(bestList);
        end_time = datetime.datetime.now();
        time_diff = (end_time - start_time);
        execution_time = time_diff.total_seconds() * 1000;
        print(f"{'Case: Best ' : <20}", end="");
        my_string = 'Size: '+str(s);
        print(f"{my_string : ^10}",end="");
        execution_time=format(execution_time,".3f");
        my_string = 'Elapsted Time: ' + str(execution_time)+' ms';
        print(f"{my_string : >30}",end="\n" );


        start_time = datetime.datetime.now()
        Example(worstList);
        end_time = datetime.datetime.now();
        time_diff = (end_time - start_time);
        execution_time = time_diff.total_seconds() * 1000;
        print(f"{'Case: Worst ' : <20}", end="");
        my_string = 'Size: ' + str(s);
        print(f"{my_string : ^10}", end="");
        execution_time = format(execution_time, ".3f");
        my_string = 'Elapsted Time: ' + str(execution_time) + ' ms';
        print(f"{my_string : >30}", end="\n");

        start_time = datetime.datetime.now()
        Example(randomList2);
        end_time = datetime.datetime.now();
        time_diff = (end_time - start_time);
        execution_time = time_diff.total_seconds() * 1000;
        print(f"{'Case: Average ' : <20}", end="");
        my_string = 'Size: ' + str(s);
        print(f"{my_string : ^10}", end="");
        execution_time = format(execution_time, ".3f");
        my_string = 'Elapsted Time: ' + str(execution_time) + ' ms';
        print(f"{my_string : >30}", end="\n");
