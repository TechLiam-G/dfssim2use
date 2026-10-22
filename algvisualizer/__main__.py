from algvisualizer import dfs
import time

if __name__ == "__main__":
    adj = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5, 6],
        3: [1, 7],
        4: [1, 8],
        5: [2, 9],
        6: [2, 10],
        7: [3, 11],
        8: [4, 12],
        9: [5],
        10: [6],
        11: [7],
        12: [8],
    }

    visited = [False] * len(adj)
    time.sleep(5)
    dfs(adj, visited, 0)

    print("DFS completed successfully!")