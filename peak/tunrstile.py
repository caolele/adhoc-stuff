"""
A university has exactly one turnstile. Unfortunately many people want to pass through the turnstile in different directions. 
The i-th person comes to turnstile at times[i] and wants to either exit the university(direction=1) or enter the university(direction=0).
People form 2 queues, one to exit one to enter. They are ordered by the time they came to turnstile and if the times are equal by their indices. 

If someone wants to enter the university and other person wants to exit at the same time, there are 3 cases. 
* if in previous second turnstile was not used (maybe it was used before not in the previous second)then the person who wants to leave goes first. 
* if in previous second the turnstile was used to exit then the person who wants to exit goes first.
* if in previous second the turnstile was used as entrance then the person who wants to enter goes first 

Passing through the turnstile takes 1 second. For each person return the time at which they pass through the turnstile. 

Example:- n = 4 (there are 4 people). 
times = [0,0,1,5] (Given in sorted order) It means that person 0 and person 1 come to turnstile at 0th second. 
direction  = [0,1,1,0] (Person 0 wants to enter while person 1 wants to exit)

Output = [2,0,1,5]

Explanation:- Person 0 and person 1 comes to turnstile at $0th second.  
Turnstile was not previously used hence person 1 passes through turntile first. 
Hence ans[1] = 0

Now person 0 and person 3 are at turnstile for second 1. 
But since turnstile was used to exit previously and person 3 wants to exit it will pass through turnstile at 1. Hence ans[2]=1. And so on.. 
"""

def turnstile_flush(times, dirs):
    n_person = len(times)
    output = [None for _ in dirs]
    turnstile_state = -1 # -1 not used; 0 entry; 1 exit
    sec = 0
    # cache for persons wating to be served (one for each direction)
    cache = ([], [])
    # iterate until there is no more person in the queue
    ptr = 0
    while ptr < n_person or len(cache[0]) > 0 or len(cache[1]) > 0:
        # add person if there is more for the current second
        while ptr < n_person:
            if times[ptr] == sec:
                _dir = dirs[ptr]
                cache[_dir].append(ptr)
                ptr += 1
            else:
                break    
        # pick one person to serve if there is qualified in cache
        if turnstile_state in {-1, 1}: # last state: idle/exit
            if len(cache[1]) > 0:
                _person = cache[1].pop(0)
                output[_person] = sec
                turnstile_state = 1
            elif len(cache[0]) > 0:
                _person = cache[0].pop(0)
                output[_person] = sec
                turnstile_state = 0
            else:
                turnstile_state = -1
        elif turnstile_state == 0: # last state: entry
            if len(cache[0]) > 0:
                _person = cache[0].pop(0)
                output[_person] = sec
                turnstile_state = 0
            elif len(cache[1]) > 0:
                _person = cache[1].pop(0)
                output[_person] = sec
                turnstile_state = 1
            else:
                turnstile_state = -1
        # increment the time
        sec += 1
    return output # [x + 1 for x in output]


if __name__ == '__main__':
    
    times = [0, 0, 1, 5]
    dirs = [0, 1, 1, 0]
    print(turnstile_flush(times, dirs))

    times = [0, 0, 0, 0, 1, 1, 3]
    dirs = [0, 0, 1, 1, 1, 0, 1]
    print(turnstile_flush(times, dirs))

    times = [0, 0, 0, 0, 1, 1, 4]
    dirs = [0, 0, 1, 1, 1, 0, 1]
    print(turnstile_flush(times, dirs))