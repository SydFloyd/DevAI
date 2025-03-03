from src.utils.task_breakdown import ProjectManager

pm = ProjectManager()

query = (
    "Create a barebones singleplayer flight sim. "
    "Nothing fancy in terms of visuals. "
    "Keybindings should allow user to increase throttle and fly the plane using typical aircraft controls."
)
outline, tasks = pm.run(query)

print("Outline:\n", outline)
print("\nTasks:\n", tasks)