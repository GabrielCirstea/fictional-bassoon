import threading
import time

def handy(n: int, share):
    print("share:", share)
    time.sleep(n)
    print("share:", share)

def worker(jobs: list):
    for j in jobs:
        print(threading.get_ident(), "Working on", j)
        time.sleep(j)

# MAKE A GOT DAMN CLASS FOR WORKERS WITH THEYR SHARED JOBS LIST
class Worker:
    def __init__(self, jobs):
        self.thread = threading.Thread(target=worker, args=(jobs,))
        self.jobs = jobs

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    def tid(self):
        return self.thread.native_id

def balance_baby(workers: Worker, target: Worker):
    for w in workers:
        if w == target:
            print("Hit the same")
            continue

def main():
    jobs1 = [23,55,34]
    jobs2 = [12,5,4]
    t1 = Worker(jobs1)
    t2 = Worker(jobs2)
  
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    t_list = [t1, t2]

    while len(t_list) > 0:
        to_pop = []
        for (i, t) in enumerate(t_list):
            if t.thread.is_alive() == False:
                print("joining {}".format( t.thread.native_id))
                t.join()
                balance_baby(t_list, t)
                to_pop.append(i)
        for i in to_pop:
            t_list.pop(i)

if __name__ == "__main__":
    main()

