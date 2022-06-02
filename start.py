import threading
import time

class Job:
    def __init__(self, name: str, arival: int, duration: int):
        self.name = name
        self.arival = arival
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

    def print_jobs(self):
        for j in self.jobs:
            print(j.name, end=" ")
        print("")

    # to be run in a thread
    def work(self):
        # optimize it with sime signals stuff
        while self.running:
            for j in self.jobs:
                print(self.name, "Worcking on", j.name)
                # round robin stuff
                slp_time = min(j.duration, self.quantum)
                time.sleep(slp_time)
                j.remaining -= slp_time
                if j.is_done():
                    self.jobs.remove(j)
        print("stoping worker:", self.name)


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
    jobs = [Job("a1",0,10),Job("a2",0,5),Job("a3",0,4), Job("a4",0,10),
            Job("b1",0,3),Job("b2",0,3),Job("b3",0,2),Job("George",1,3)]
    n_workers = 3
    slice_p = len(jobs)//n_workers
    jobs_w = []

    for i in range(n_workers):
        jobs_w.append(jobs[slice_p*i : slice_p*i + slice_p])
    for i in range(len(jobs)%n_workers):
        start = len(jobs) - len(jobs)%n_workers
        jobs_w[i].append(jobs[start+i])

    workers = []
    for i in range(n_workers):
        t = Worker(jobs_w[i], f"worker{i}")
        t.print_jobs()
        workers.append(t)
  
    for w in workers:
        w.start()

    while len(workers) > 0:
        to_pop = []
        for (i, t) in enumerate(workers):
            # first try to give something else to work on
            if t.is_working() == False:
                balance_baby(workers, t)
            if t.is_working() == False:
                print("joining {}".format( t.thread.native_id))
                t.stop()
                t.join()
                to_pop.append(i)
        for i in to_pop:
            if i < len(workers):
                workers.pop(i)

if __name__ == "__main__":
    main()

