from enum import Enum

class AgentTask(Enum):
    """
    Represents the status of an agent task.
    """
    TASK_ANALYZER = "task_analyzer"
    UI_PLANNER = "ui_planner"
    UI_BUILDER = "ui_builder"
    UI_CRITIC = "ui_critic"