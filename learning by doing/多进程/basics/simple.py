import multiprocessing
import multiprocessing_import_worker


def worker():
    """worker function"""
    print('Worker')


def worker1(num):
    """thread worker function"""
    print('Worker:', num)

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        # p = multiprocessing.Process(target=worker)
        # p = multiprocessing.Process(target=worker1, args=(i,))
        p = multiprocessing.Process(target=multiprocessing_import_worker.worker,)
        jobs.append(p)
        print(jobs)
        p.start()