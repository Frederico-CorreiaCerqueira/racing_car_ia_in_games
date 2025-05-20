import numpy as np
import matplotlib.pyplot as plt

def compare_trajectories(traj1, traj2):
    """
    traj1 and traj2: list of (x, y) tuples
    """
    min_len = min(len(traj1), len(traj2))
    traj1 = traj1[:min_len]
    traj2 = traj2[:min_len]

    errors = [np.linalg.norm(np.array(p1) - np.array(p2)) for p1, p2 in zip(traj1, traj2)]
    cumulative_error = np.sum(errors)

    print(f"Cumulative trajectory error: {cumulative_error:.2f}")

    plt.plot(errors, label="Frame-by-frame error")
    plt.title("Trajectory Deviation over Time")
    plt.xlabel("Frame")
    plt.ylabel("Distance Error (pixels)")
    plt.legend()
    plt.grid(True)
    plt.show()

    return cumulative_error