# Balancing

## Jobs

Create a number of jobs of N seconds each

Can create more type of jobs, with different duration

## Running

Start some `workers` as threads (subprocess) to run the jobs

## Balancing

There i a good chance that some workers will finish before others, if that is the
case, take some jobs from other workers and give them to the sleeping ones.
