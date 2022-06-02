import threading
import time

class Job:
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration
        self.remaining = duration

    def is_done(self):
        if self.remaining <= 0:
            return True
        return False


class Worker:
    def __init__(self, jobs, name = "no_name"):
        self.thread = threading.Thread(target=self.work, args=())
        self.name = name
        self.jobs = jobs
        self.running = True
        self.quantum = 2

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    def get_tid(self):
        return self.thread.native_id

    def is_working(self):
        if len(self.jobs) > 0:
            return True
        return False

    def stop(self):
        self.running = False

    # to be run in a thread
    def work(self):
        # optimize it with sime signals stuff
        while self.running:
            for j in self.jobs:
                print(self.name, "Working on", j.name)
                # round robin stuff
                slp_time = min(j.duration, self.quantum)
                time.sleep(slp_time)
                j.remaining -= slp_time
                if j.is_done():
                    self.jobs.remove(j)
        print("Stoping worker:", self.name)


def balance_baby(workers: Worker, target: Worker):
    for w in workers:
        if w == target:
            print("Hit the same")
            continue
        if w.is_working() and len(w.jobs) > 1:
            target.jobs.append(w.jobs[-1])
            w.jobs.pop(-1)
            break

def main():
    jobs1 = [Job("a1",10), Job("a2",5), Job("a3",4), Job("a4",10)]
    jobs2 = [Job("b1",3), Job("b2",3), Job("b3",2)]
    t1 = Worker(jobs1, "worker1")
    t2 = Worker(jobs2, "worker2")
  
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    t_list = [t1, t2]

    while len(t_list) > 0:
        to_pop = []
        for (i, t) in enumerate(t_list):
            # first try to give something else to work on
            if t.is_working() == False:
                balance_baby(t_list, t)
            if t.is_working() == False:
                print("joining {}".format( t.thread.native_id))
                t.stop()
                t.join()
                to_pop.append(i)
        for i in to_pop:
            if i < len(t_list):
                t_list.pop(i)

if __name__ == "__main__":
    main()

