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
        self.alg = self.priority_based

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

def main():

    file_path = "tasks1.txt"
    jobs = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            print(line.strip("\n"))
            job = read_job(line)
            if job:
                jobs.append(job)

    jobs.sort(key=lambda x : x.arival)
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

