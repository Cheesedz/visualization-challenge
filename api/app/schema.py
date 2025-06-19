from typing import List, Optional, Literal, Union, Dict
from pydantic import BaseModel, HttpUrl

class Chat(BaseModel):
    content: str

# === Task Analyzer Agent ===

class TaskTypeInfo(BaseModel):
    type: str
    description: str


class InputOutput(BaseModel):
    input: str
    output: str


class InputFormatField(BaseModel):
    type: str
    encoding: Optional[str]
    description: Optional[str]


class InputFormat(BaseModel):
    type: str
    structure: Dict[str, InputFormatField]


class OutputFormat(BaseModel):
    type: str
    description: Optional[str]
    post_processing: Optional[Dict[str, str]]
    guidance: Optional[List[str]]


class ModelInfo(BaseModel):
    api_url: HttpUrl
    name: str
    input_format: InputFormat
    output_format: OutputFormat


class VisualizationField(BaseModel):
    name: str
    description: str


class VisualizationFeature(BaseModel):
    name: Literal["list_display", "input_function"]
    description: str
    fields: Optional[List[VisualizationField]] = None
    steps: Optional[List[str]] = None


class Visualization(BaseModel):
    description: str
    features: List[VisualizationFeature]


class Dataset(BaseModel):
    data_path: str
    description: str
    supported_formats: List[str]
    other_data: Optional[str]


class TaskAnalyzerOutput(BaseModel):
    task_type: TaskTypeInfo
    input_output: InputOutput
    model_info: ModelInfo
    visualization: Visualization
    dataset: Optional[Dataset]


# === UI Planner Agent ===

class IOField(BaseModel):
    name: str
    type: Literal["file", "text", "image", "audio", "number", "list", "label"]
    accept: Optional[List[str]] = None  # e.g. [".jpg", ".png"]
    multiple: Optional[bool] = False
    optional: Optional[bool] = False
    help_text: Optional[str] = None
    format: Optional[str] = None  # e.g., "percentage" for output


class InputSpec(BaseModel):
    description: str
    types: List[IOField]


class OutputSpec(BaseModel):
    description: str
    types: List[IOField]


class ModelFormat(BaseModel):
    type: Literal["json"]
    fields: Dict[str, str]  # field_name -> data_type/description


class ModelInfo(BaseModel):
    name: str
    description: Optional[str]
    api_url: str
    method: Literal["POST", "GET"]
    input_format: ModelFormat
    output_format: ModelFormat


class UIHints(BaseModel):
    layout: Literal["responsive_card", "wizard", "dashboard"]
    components: List[str]  # e.g., file_upload, button, result_table
    theme: Optional[Dict[str, str]]  # e.g., {"primary_color": "#0057FF"}


class VisualizationFeature(BaseModel):
    description: str
    steps: Optional[List[str]] = None
    fields: Optional[List[str]] = None


class Visualization(BaseModel):
    features: Dict[str, VisualizationFeature]


class DatasetInfo(BaseModel):
    name: Optional[str]
    description: Optional[str]
    source: Optional[str]
    path: str
    format: str


class Accessibility(BaseModel):
    keyboard: bool = True
    screen_reader: bool = True
    alt_text_required: bool = True


class ErrorHandling(BaseModel):
    invalid_input: Optional[str]
    missing_input: Optional[str]
    api_error: Optional[str]


class TaskMeta(BaseModel):
    title: str
    description: str
    version: Optional[str] = "1.0"
    created_by: Optional[str] = None


class UIPlannerOutput(BaseModel):
    task_type: str
    meta: TaskMeta

    input_spec: InputSpec
    output_spec: OutputSpec

    model: ModelInfo
    ui_hints: UIHints
    visualization: Visualization

    dataset_info: Optional[DatasetInfo]
    accessibility: Optional[Accessibility]
    error_handling: Optional[ErrorHandling]


class UIAgentOutput(BaseModel):
    html: str
    css: str
    js: str
