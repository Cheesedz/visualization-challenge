def set_task_analyzer_prompt(task_spec):
    """
    Set the prompt for the task of analyzing a given task specification.
    """
    return f"""
        Analyze the following task.yaml file and extract its structure into a well-formatted JSON object:

        Task Specification: {task_spec}
        """
        
def set_task_ui_planner_prompt(task_desc):
    """
    Set the prompt for the task of planning a user interface based on a given task specification.
    """
    return f"""
        Given the following task structure, generate the corresponding UI Blueprint:

        Task Description: {task_desc}
        """
        
def set_task_ui_builder_prompt(task_desc):
    """Set the prompt for the task of building a user interface based on a given task specification.
    """
    return f"""
        Given the following task structure, generate the corresponding UI code:

        Task Description: {task_desc}
        """
        