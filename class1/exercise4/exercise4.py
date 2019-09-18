#!/usr/bin/env python

from nornir import InitNornir


def my_first_task(task):
    print("Finally learning Nornir!")
    print(task.host)

def main():
    nr = InitNornir()
    nr.run(task=my_first_task)

if __name__=="__main__":
    main()
