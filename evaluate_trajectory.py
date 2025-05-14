import pickle
from utils.trajectory_comparison import compare_trajectories

# Load trajectories
with open("trajectories.pkl", "rb") as f:
    data = pickle.load(f)

player_traj = data["player"]
ai_traj = data["ai"]

# Compare
compare_trajectories(player_traj, ai_traj)