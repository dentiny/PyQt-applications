# Counter
from collections import Counter;
counter=Counter(['a','a','a','b','b','c']);

# most common
common_list=counter.most_common();
most_common=counter.most_common(1)[0];

# count
count=counter['a'];

# operation of counters
counter1=Counter(['a','b','b','c','c','c']);
sum_counter=counter+counter1;
diff_counter=counter-counter1;

# deque
from collections import deque;
dq=deque(['a','b','c']);

# pop & popleft
while(len(dq)>1):
    left_s=dq.popleft();
    right_s=dq.pop();
    
# append & appendleft
dq.append('d');
dq.appendleft('d');

# extend & extendleft
dq.extend(['a','b','c']);
dq.extendleft(['a','b','c']);

# index 
index=dq.index('a');

# reverse
dq=reversed(dq);
dq.reverse();

# rotate
dq.rotate(1);

# for num>0: right direaction
# for num<0: left direction
    
# max length
# dq=deque(list,maxlen=num);
# dq=deque([],maxlen=5);

# heap
import heapq;

# largest & smallest
# list
largest=heapq.nlargest(2,[1,2,3,4,5]);
smallest=heapq.smallest(2,[1,2,3,4,5]);

# dictionary
infor=[{"name":"Ethan","number":10},{"name":"jianghao","number":100}];
cheap=heapq.nsmallest(1,infor,key=lambda s:s["number"]);
expensive=heapq.nlargest(1,infor,key=lambda s:s["number"]);

# ascendent order
nums=[1,2,3,4,5];
heapq.heapify(nums);
ordered_list=[];
while(True):
    try:
        ordered_list.append(heapq.heappop(nums));
    except:
        break;
 
 # defaultdict
 from collections import defaultdict;

# default string dictionary
d=defaultdict(str);
d['a']+='jianghao';
d['b']+='ethan';

# default int dictionary
d=defaultdict(int);
d['a']+=1;
d['b']+=2;

# default list dictionary
d=defaultdict(list);
d['a'].append("jianghao");
d['b'].append("ethan");

# default dictionary dictionary
d=defaultdict(dict);
d['a']['name']="jianghao";
d['b']['name']="ethan";

# default set dictionary
d=defaultdict(set);
d['a'].add("jianghao");
d['b'].add("ethan");
