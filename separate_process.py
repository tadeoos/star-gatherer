#!/usr/bin/env python

import os, pickle
def run_in_separate_process(func, *args, **kwds):
    pread, pwrite = os.pipe()
    pid = os.fork()
    if pid > 0:
        os.close(pwrite)
        with os.fdopen(pread, 'rb') as f:
            status, result = pickle.load(f)
        os.waitpid(pid, 0)
        if status == 0:
            return result
        else:
            raise result
    else:
        os.close(pread)
        try:
            result = func(*args, **kwds)
            status = 0
        except Exception as exc:
            result = exc
            status = 1
        with os.fdopen(pwrite, 'wb') as f:
            try:
                pickle.dump((status,result), f, pickle.HIGHEST_PROTOCOL)
            except pickle.PicklingError as exc:
                pickle.dump((2,exc), f, pickle.HIGHEST_PROTOCOL)
        os._exit(0)

#an example of use
def treble(x):
    return 3 * x

def main():
    #calling directly
    print(treble(4))
    #calling in separate process
    print(run_in_separate_process(treble, 4))
