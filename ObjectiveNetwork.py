# This class handles all of the Objective Network handling
# Board Game Scholar Post #5
# Freddy Reiber

class TaskNetwork:

    def __init__(self):
        self.tasksLeft = 0
        self.currentTaskNumber = 1
        self.totalTasks  = 0
        self.freeTasks = []
        self.numberTasks = [None] * 10
        self.orderTasks = []
        self.lastTask = None

    # This adds the Task to the proper value. The Logic here is a bit confusing, but is explained later.
    def addTask(self, newTask):
        if newTask.taskToken == 0:
            self.freeTasks.append(newTask)
        elif newTask.taskToken > 0 and newTask.taskToken < 10:
            self.numberTasks[newTask.taskToken] = newTask
        elif newTask.taskToken == - 1:
            self.lastTask = newTask
        elif newTask.taskToken > 10:
            self.orderTasks.append(newTask)
        self.tasksLeft += 1
        self.totalTasks += 1

    def isComplete(self):
        self.updateTasks()
        if self.tasksLeft == 0:
            return True
        return False

    def updateTasks(self):
        tasksCompleted = 0
        for task in self.freeTasks:
            if task.isComplete():
                tasksCompleted += 1
        for task in self.orderTasks:
            if task.isComplete():
                tasksCompleted += 1
        self.currentTaskNumber = tasksCompleted + 1
        self.tasksLeft = self.totalTasks - tasksCompleted

    def getPossibleTasks(self):
        # First we update the task list, as we may have completed one last hand.
        self.updateTasks()
        # Check if there is a last task, and we only have 1 left
        if self.lastTask is not None and self.tasksLeft == 1:
            return [self.lastTask]
        # Check if we must solve a certain task this turn
        if self.numberTasks[self.currentTaskNumber] is not None:
            return [self.numberTasks[self.currentTaskNumber - 1]]
        # If we don't have a task we must solve, then we can generate a list of possible objectives to complete.
        # First we get the first item in the order task
        possibleTasks = []
        for task in self.orderTasks:
            if not task.isComplete():
                possibleTasks.append(task)
                break
        # Then all of the other tasks if free tasks can be added
        for task in self.freeTasks:
            if not task.isComplete():
                possibleTasks.append(task)
        return possibleTasks

