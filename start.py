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
    def __init__(self, jobs, name = "no_name", alg = "robin"):
        self.thread = threading.Thread(target=self.work, args=())
        self.cur_time = 1
        self.name = name
        self.jobs = jobs
        self.running = True
        self.quantum = 2
        self.cur_task = None
        self.chose_alg(alg)

    def chose_alg(self, alg: str):
        if alg == "robin":
            self.alg = self.round_robin
        elif alg == "FCFS":
            self.alg = self.FCFS
        elif alg == "priority":
            self.alg = self.priority_based
        elif alg == "SJF":
            self.alg = self.SJF

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

    def pretty(self):
        print(f"{self.name}")
        print("#" * len(self.jobs))
        if self.cur_task:
            print(f"Wroking on {self.cur_task.name} - {self.cur_task.remaining}/{self.cur_task.duration}")
        else:
            print("Sleeping")

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
            self.cur_task = j
            # round robin stuff
            slp_time = j.duration
            self.step_task(slp_time)
            j.remaining -= slp_time
            if j.is_done():
                self.jobs.remove(j)
        if len(self.jobs) < 1:
            self.cur_task = None

    def round_robin(self):
        for j in self.jobs:
            #print(self.name, "Working on", j.name)
            self.cur_task = j
            # round robin stuff
            slp_time = min(j.duration, self.quantum)
            self.step_task(slp_time)
            j.remaining -= slp_time
            if j.is_done():
                self.jobs.remove(j)
        if len(self.jobs) < 1:
            self.cur_task = None

    # sortest job first
    def SJF(self):
        if len(self.jobs) < 1:
            return
        next_j = min(self.jobs, key=lambda j : j.duration)
        print(self.name, "Working on", next_j.name, next_j.duration)
        self.cur_task = next_j
        self.step_task(next_j.duration)
        self.jobs.remove(next_j)
        if len(self.jobs) < 1:
            self.cur_task = None

    def priority_based(self):
        if len(self.jobs) < 1:
            return
        next_j = min(self.jobs, key=lambda j : j.priority)
        print(self.name, "Working on", next_j.name, next_j.duration)
        self.cur_task = next_j
        self.step_task(next_j.duration)
        self.jobs.remove(next_j)
        if len(self.jobs) < 1:
            self.cur_task = None


def balance_baby(workers: Worker, target: Worker):
    for w in workers:
        if w == target:
            #print("Hit the same")
            continue
        if w.is_working() and len(w.jobs) > 1:
            for j in w.jobs:
                if j == w.cur_task:
                    continue
                target.jobs.append(j)
                w.jobs.remove(j)
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
    for i in reversed(to_remove):
        all_jobs.pop(i)
    return jobs

# one by one to each worker
def spread_jobs(jobs, workers):
    #print("spreding")
    while len(jobs) > 0:
        for w in workers:
            if len(jobs) > 0:
                print(f"give job {jobs[0].name} to {w.name}")
                w.jobs.append(jobs.pop(0))
            else:
                break

def least_used(jobs, workers):
    while len(jobs) > 0:
        min_j = len(workers[0].jobs)
        the_worker = workers[0]
        for w in workers:
            if len(w.jobs) < min_j:
                min_j = len(w.jobs)
                the_worker = w
        the_worker.jobs.append(jobs.pop(0))

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
        t = Worker([], f"worker{i}", alg="FCFS")
        t.print_jobs()
        workers.append(t)

    spread_jobs(jobs, workers)
  
    for w in workers:
        w.start()

    while len(workers) > 0 or len(all_jobs) > 0:
        quantum = workers[0].cur_time
        if len(all_jobs) > 0:
            jobs = take_jobs(all_jobs, quantum)
            least_used(jobs, workers)
        to_pop = []
        time.sleep(1)
        print("quantum:", quantum)
        print("-" * 20)
        for (i, t) in enumerate(workers):
            # first try to give something else to work on
            if t.is_working() == False:
                balance_baby(workers, t)
            t.pretty()
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
