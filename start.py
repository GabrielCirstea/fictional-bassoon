import threading
import time

def handy(n: int, share):
    print("share:", share)
    time.sleep(n)
    print("share:", share)

def worker(jobs: list):
    for j in jobs:
        print(threading.get_ident(), "Worcking on", j.name)
        time.sleep(j.duration)

class Job:
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration

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

    def is_working(self):
        if len(self.jobs) > 0:
            return True
        return False

def balance_baby(workers: Worker, target: Worker):
    for w in workers:
        if w == target:
            print("Hit the same")
            continue
        if not w.is_working():
            target.jobs.append(w.jobs[-1])
            w.jobs.pop(-1)
            target.start()
            break

def main():
    jobs1 = [Job("a1",23),Job("a2",5),Job("a3",4), Job("a4",10)]
    jobs2 = [Job("b1",6),Job("b2",3),Job("b3",2)]
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
            # first try to give something else to work on
            if t.thread.is_alive() == False:
                balance_baby(t_list, t)
            if t.thread.is_alive() == False:
                print("joining {}".format( t.thread.native_id))
                t.join()
                to_pop.append(i)
        for i in to_pop:
            t_list.pop(i)

if __name__ == "__main__":
    main()

