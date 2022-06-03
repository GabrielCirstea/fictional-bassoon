#!/usr/bin/python3
import threading
import time

class Job:
    def __init__(self, name: str, arival: int, duration: int, priority: int):
        self.name = name
        self.arival = arival
        self.duration = duration
        self.remaining = duration
        self.priority = priority

    def is_done(self):
        if self.remaining <= 0:
            return True
        return False


class Worker:
    def __init__(self, jobs, name = "no_name"):
        self.thread = threading.Thread(target=self.work, args=())
        self.cur_time = 1
        self.name = name
        self.jobs = jobs
        self.running = True
        self.quantum = 2
        self.alg = self.FCFS

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

    # run the thread until is semnaled to stop
    def work(self):
        # optimize it with sime signals stuff
        while self.running:
            self.alg()
        print("Stoping worker:", self.name)

    # do the task, update the current time
    def step_task(self, duration: int):
        time.sleep(duration//2)
        self.cur_time += duration

    # first come first serverd
    def FCFS(self):
        for j in self.jobs:
            print(self.name, "Working on", j.name)
            # round robin stuff
            slp_time = j.duration
            self.step_task(slp_time)
            j.remaining -= slp_time
            if j.is_done():
                self.jobs.remove(j)

    def round_robin(self):
        for j in self.jobs:
            print(self.name, "Working on", j.name)
            # round robin stuff
            slp_time = min(j.duration, self.quantum)
            self.step_task(slp_time)
            j.remaining -= slp_time
            if j.is_done():
                self.jobs.remove(j)

    # sortest job first
    def SJF(self):
        if len(self.jobs) < 1:
            return
        next_j = min(self.jobs, key=lambda j : j.duration)
        print(self.name, "Working on", next_j.name, next_j.duration)
        self.step_task(next_j.duration)
        self.jobs.remove(next_j)

    def priority_based(self):
        if len(self.jobs) < 1:
            return
        next_j = min(self.jobs, key=lambda j : j.priority)
        print(self.name, "Working on", next_j.name, next_j.duration)
        self.step_task(next_j.duration)
        self.jobs.remove(next_j)


def balance_baby(workers: Worker, target: Worker):
    for w in workers:
        if w == target:
            print("Hit the same")
            continue
        if w.is_working() and len(w.jobs) > 1:
            target.jobs.append(w.jobs[-1])
            w.jobs.pop(-1)
            break

def read_job(line: str):
    fields = line.split(",")
    try:
        name = fields[0].strip(" ")
        arival = int(fields[1].strip(" "))
        duration = int(fields[2].strip(" "))
        priority = int(fields[3].strip(" "))
        return Job(name, arival, duration, priority)
    except:
        return None

def take_jobs(all_jobs, quantum):
    jobs = []
    to_remove = []
    for (i,j) in enumerate(all_jobs):
        if j.arival <= quantum:
            jobs.append(j)
            to_remove.append(i)
    for i in to_remove:
        all_jobs.pop(i)
    return jobs

# one by one to each worker
def spread_jobs(jobs, workers):
    print("spreding")
    while len(jobs) > 0:
        for w in workers:
            if len(jobs) > 0:
                print(f"give job {jobs[0].name} to {w.name}")
                w.jobs.append(jobs.pop(0))

def main():

    file_path = "tasks1.txt"
    all_jobs = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            job = read_job(line)
            if job:
                all_jobs.append(job)

    all_jobs.sort(key=lambda x : x.arival)
    quantum = 1
    n_workers = 3

    jobs = take_jobs(all_jobs, quantum)

    workers = []
    for i in range(n_workers):
        t = Worker([], f"worker{i}")
        t.print_jobs()
        workers.append(t)

    spread_jobs(jobs, workers)
  
    for w in workers:
        w.start()

    while len(workers) > 0 or len(all_jobs) > 0:
        quantum = workers[0].cur_time
        if len(all_jobs) > 0:
            jobs = take_jobs(all_jobs, quantum)
            spread_jobs(jobs, workers)
        to_pop = []
        time.sleep(1)
        print("quantum:", quantum)
        for (i, t) in enumerate(workers):
            # first try to give something else to work on
            #if t.is_working() == False:
                #balance_baby(workers, t)
            if t.is_working() == False and len(all_jobs) < 1:
                print("joining {}".format( t.thread.native_id))
                t.stop()
                t.join()
                to_pop.append(i)
        for i in to_pop:
            if i < len(workers):
                workers.pop(i)

if __name__ == "__main__":
    main()
