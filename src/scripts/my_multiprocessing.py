import multiprocessing


def worker(conn):
    data = conn.recv()
    print("Received:", data)
    conn.send("Message received!")

if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=worker, args=(child_conn,))
    p.start()
    parent_conn.send("Hello from main process!")
    print(parent_conn.recv())
    p.join()