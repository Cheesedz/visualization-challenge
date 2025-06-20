from enum import Enum

class AgentTask(Enum):
    """
    Represents the status of an agent task.
    """
    TASK_ANALYZER = "task_analyzer"
    UI_PLANNER = "ui_planner"
    UI_BUILDER = "ui_builder"
    UI_CRITIC = "ui_critic"
    
class ProblemTask(Enum):
    """
    Represents the status of an agent task.
    """
    TEXT_CLASSIFICATION = "Text classification"
    IMAGE_CLASSIFICATION = "Image classification"
    AUDIO_CLASSIFICATION = "Audio classification"
    OBJECT_DETECTION = "Object detection in image"
    TABULAR_QUESTION_ANSWERING = "Tabular Question Answering"