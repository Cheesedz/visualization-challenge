from app.config import GROQ_API_KEY, MODEL_NAME
from groq import AsyncGroq

import json
import textgrad as tg

from app.util import logger
from app.constant import AgentTask
from app.prompt import set_task_analyzer_prompt, set_task_ui_builder_prompt, set_task_ui_planner_prompt
from app.schema import TaskAnalyzerOutput, UIAgentOutput, UIPlannerOutput
import asyncio

class LLMPipeline:
  
    def __init__(self):
        self.client = AsyncGroq(
            api_key=GROQ_API_KEY
        )
        # set the backward model to evaluate the summaries
        tg.set_backward_engine("groq-llama3-70b-8192", override=True)

        self.role_prompts = {
            AgentTask.TASK_ANALYZER : '''
                You are a Task Analyzer Agent. Your job is to read a YAML file that defines a machine learning task, and output a standardized JSON format including task type, input/output formats, model information, visualization features, and dataset description.
                Respond only with JSON using this format:
                """
                {
                    "task_type": {
                        "type": "string", 
                        "description": "string"
                    },
                    "input_output": {
                        "input": "string",
                        "output": "string"
                    },
                    "model_info": {
                        "api_url": "string",
                        "name": "string",
                        "input_format": {
                        "type": "json | base64 | multipart | ...",
                        "structure": {
                            "key": {
                            "type": "string",
                            "encoding": "optional string",
                            "description": "string"
                            }
                        }
                        },
                        "output_format": {
                        "type": "array | json | string",
                        "description": "string",
                        "post_processing": {
                            "optional string key": "description"
                        },
                        "guidance": ["step1", "step2"]
                        }
                    },
                    "visualization": {
                        "description": "string",
                        "features": [
                        {
                            "name": "list_display | input_function",
                            "description": "string",
                            "fields": [
                            { "name": "string", "description": "string" }
                            ],
                            "steps": ["optional steps"]
                        }
                        ]
                    },
                    "dataset": {
                        "data_path": "string",
                        "description": "string",
                        "supported_formats": ["jpg", "png", ...],
                        "other_data": "optional string"
                    }
                }
                """
            ''',
            AgentTask.UI_PLANNER: '''
                You are a UI Planner Agent. Based on a task description, generate a clean UI Blueprint schema. The schema should define layout, input fields, output display types, and API interaction settings. 
                Ensure the task description is clearly kept again and the UI is user-friendly, especially the output format and model input structure.
                Your output must be valid JSON, matching a UI schema format like this:
                """
                    {
                        "title": "string",
                        "description": "string",
                        "task_description": "string",
                        "layout": "responsive_card | wizard | dashboard",
                        "navbar": [
                            { "label": "string", "target": "#anchor_id" }
                        ],
                        "inputs": [
                            {
                            "type": "file_upload | text_input | dropdown",
                            "label": "string",
                            "accept": ["jpg", "png"],
                            "drag_and_drop": true,
                            "input_id": "string"
                            }
                        ],
                        "actions": [
                            {
                            "type": "button",
                            "label": "string",
                            "on_click": "string (handler name)"
                            }
                        ],
                        "api_call": {
                            "url": "string",
                            "method": "POST",
                            "input_structure": {
                                "field": "value"
                            },
                            "response_mapping": {
                                "label": "predicted_label",
                                "score": "probability"
                            }
                        },
                        "outputs": [
                            {
                            "type": "image_result | table | text_block",
                            "output_id": "string",
                            "fields": [
                                { "name": "string", "label": "string", "type": "text | image | bar" }
                            ],
                            "list_display": true
                            }
                        ],
                        "dataset_info": {
                            "description": "string",
                            "path": "string",
                            "formats": ["jpg", "png"],
                            "label_mapping": "optional string"
                        },
                        "footer": {
                            "info": "string",
                            "api_url": "string",
                            "version": "string"
                        },
                        "visualization_features": {
                            "image_preview": true,
                            "probability_bar": true,
                            "list_display": true
                        },
                        "accessibility": {
                            "keyboard_navigation": true,
                            "screen_reader": true
                        },
                        "error_handling": {
                            "invalid_format": "string",
                            "empty_upload": "string",
                            "api_error": "string"
                        }
                    }
                """
            ''',
            AgentTask.UI_BUILDER: '''
                You are a UI Generator Agent. Given a UI Blueprint, you must generate working HTML, CSS, JS code with highly interactive components. The component should allow users to input data, call the model API asynchronously and avoid CORS errors, then display the output results as specified. Focus on task description for not missing any steps and ensure the API url correctly.
                Note that if the task related to image, image must be convert to base64 string and passed to the model API.
                Double check the input structure and output mapping to ensure the API call is correct.
                Don't use any external libraries, just use pure HTML, CSS, JS.
                Some real response form for the task you can use to handle the response properly:
                - text_classification: 
                    "data": [
                        [
                            {
                                "label": "anger",
                                "score": 0.006408268585801125
                            },
                            ...
                        ]
                    ]
                Respond only in JSON string with html, css, js in only one code block with below format:
                """
                {
                    "code": "<!DOCTYPE html>\\n<html>\\n<head>\\n<style>body { font-family: Arial; }</style>\\n</head>\\n<body>\\n<input type=\\\"file\\\" id=\\\"imageInput\\\" />\\n<button onclick=\\\"sendImage()\\\">Submit</button>\\n<pre id=\\\"output\\\"></pre>\\n<script>function sendImage() { const reader = new FileReader(); reader.onload = function() { fetch('/api/model', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ image: reader.result }) }).then(res => res.json()).then(data => document.getElementById('output').innerText = JSON.stringify(data, null, 2)); }; reader.readAsDataURL(document.getElementById('imageInput').files[0]); }</script>\\n</body>\\n</html>"
                }
                """
            ''',
            AgentTask.UI_CRITIC: '''
                You are a UI Critic Agent, a master code reviewer. You will review HTML, CSS, JS code in a given code block and provide feedback about its usability, completeness, possible bugs, and improve it. 
                Respond with the optimized code ensure has enough HTML, CSS, JS, API called asynchronously, especially focusing on handling response data from the model API, syntax correctness and displaying it in the UI.
                Don't use any external libraries, just use pure HTML, CSS, JS.
                Some real response form for the task you can use to review the response handling properly:
                - text_classification: 
                    "data": [
                        [
                            {
                                "label": "anger",
                                "score": 0.006408268585801125
                            },
                            ...
                        ]
                    ]
            '''
        }
        return None
  
    def get_model_schema(self, task):
        if task == AgentTask.TASK_ANALYZER:
            return json.dumps(TaskAnalyzerOutput.model_json_schema(), indent=2)
        elif task == AgentTask.UI_PLANNER:
            return json.dumps(UIPlannerOutput.model_json_schema(), indent=2)
        elif task == AgentTask.UI_BUILDER:
            return json.dumps(UIAgentOutput.model_json_schema(), indent=2)
        return None
    

    def get_role_prompt(self, task):
        return self.role_prompts.get(task, None)
    
    def set_prompt(self, input, task):
        match(task):
            case AgentTask.TASK_ANALYZER:
                return set_task_analyzer_prompt(input)
            case AgentTask.UI_PLANNER:
                return set_task_ui_planner_prompt(input)
            case AgentTask.UI_BUILDER:
                return set_task_ui_builder_prompt(input)
            case _:
                raise ValueError(f"Unknown task type: {task}")

    def _set_evaluation_instruction(self, task, transcript, response_feedback=None):
        prompt = self.set_prompt(transcript, task = "summary")

        if task == "summary":
            self.evaluation_instruction = f"""
            Here's a paragraph of podcast transcript: {transcript}. Evaluate the summary of this transcript, be smart, logical, and very critical. Just provide concise and general feedback.
            """
        elif task == "prompt":
            self.evaluation_instruction = f"""
            Here's the prompt to summarize: {prompt}. Evaluate the prompt based on the following response feedback ${response_feedback}, be smart, logical, and very critical. Just provide concise and general feedback.
            """
        return None
  
    def _set_optimization_instruction(self, task_desc, initial_code, response_feedback):
        prompt = self.set_prompt(task_desc, task = AgentTask.UI_BUILDER)
        self.evaluation_instruction = f"""
            Here's the prompt to optimized: {prompt}. 
            The intial code generated by the above prompt is: 
            ${initial_code}
            Evaluate the prompt based on the following response feedback:
            ${response_feedback}
            Be smart, logical, and very critical. Just provide concise and general feedback."""
        
        return None
        
    async def generate_content(self, task, prompt):
        print(f"Model name: {MODEL_NAME}")
        if not MODEL_NAME:
            raise ValueError("MODEL_NAME is not set. Please set it in the config file.")
        chat_completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"{self.get_role_prompt(task)}\n"
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=MODEL_NAME,
                temperature=0,
                stream=False,
                response_format={"type": "json_object"},
            )
        return chat_completion.choices[0].message.content

    async def task_analyze(self, task_spec: str) -> TaskAnalyzerOutput | None:
        prompt = self.set_prompt(task_spec, task=AgentTask.TASK_ANALYZER)
        try:
            processed_task = await self.generate_content(task=AgentTask.TASK_ANALYZER, prompt=prompt)
            logger.info('[Task Analyzer] - Processed task: %s', processed_task)
        except Exception as e:
            print(e)
            return {"error": "Invalid JSON response from the model."}
        return processed_task

    async def ui_planner(self, task_desc: str) -> UIPlannerOutput | None:
        prompt = self.set_prompt(task_desc, task=AgentTask.UI_PLANNER)
        try:
            raw_plan = await self.generate_content(task=AgentTask.UI_PLANNER, prompt=prompt)
            logger.info('[UI Planner] - UI Plan: %s', raw_plan)
        except Exception as e:
            print(e)
            return {"error": "Invalid JSON response from the model."}
        return raw_plan

    async def ui_builder(self, plan, optimize=False):
        prompt = self.set_prompt(plan, task=AgentTask.UI_BUILDER)
        initial_code = None
        response_feedback = None
        try:
            content = await self.generate_content(task=AgentTask.UI_BUILDER, prompt=prompt)
            code = UIAgentOutput.model_validate_json(content)
            logger.info('[UI Builder] - Generated code: %s', code)
            initial_code = code
        except Exception as e:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    prompt = self.set_prompt(plan, task=AgentTask.UI_BUILDER)
                    content = await self.generate_content(task=AgentTask.UI_BUILDER, prompt=prompt)
                    logger.info('[UI Builder] - Retries generated code: %s', content)
                    # code = UIAgentOutput.model_validate_json(content)
                    initial_code = content
                    break
                except Exception as retry_e:
                    if attempt == max_retries - 1:
                        logger.error('[UI Builder] - Failed to generate code after retries: %s', retry_e)
                        return {"error": "Invalid JSON response from the model after retries."}
                    await asyncio.sleep(1.5)
        if optimize:
            # _optimize_code is async, so just await it directly
            final_code = await self._optimize_code(plan, initial_code)
        else:
            final_code = initial_code
        return final_code
    

    async def _optimize_code(self, original_input, initial_code):
        if hasattr(initial_code, "model_dump"):
            serializable_code = initial_code.model_dump()
        else:
            serializable_code = initial_code
        input_code = tg.Variable(json.dumps(serializable_code),
                role_description=self.get_role_prompt(AgentTask.UI_CRITIC),
                requires_grad=True)
        self._set_optimization_instruction(original_input, initial_code, response_feedback=None)
        self.optimizer = tg.TGD(parameters=[input_code])

        # TextLoss is a natural-language specified loss function that describes
        # how we want to evaluate the reasoning.
        loss_fn = tg.TextLoss(self.evaluation_instruction)

        # Step 3: Do the loss computation, backward pass, and update the punchline.
        # Exact same syntax as PyTorch!
        loss = loss_fn(input_code)
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()
        
        logger.info(vars(input_code))
        logger.info("%s Nothing here", input_code.get_gradient_text())
        logger.info("Loss value: %s", loss.value)
    
        logger.info("Optimized code: %s", input_code.value)
        try:
            return json.loads(input_code.value)
        except Exception:
            return input_code.value
    
    def _optimize_prompt(self, article, initial_summary, response_feedback):
        prompt = self.set_prompt(article, task = "summary")
        input_prompt = tg.Variable(prompt,
                        role_description="initial prompt for LLM to evaluate",
                        requires_grad=True)
        self._set_evaluation_instruction(task = "prompt", transcript = initial_summary, response_feedback=response_feedback)
        self.optimizer = tg.TGD(parameters=[input_prompt])


        # TextLoss is a natural-language specified loss function that describes
        # how we want to evaluate the reasoning.
        loss_fn = tg.TextLoss(self.evaluation_instruction)

        # Step 3: Do the loss computation, backward pass, and update the punchline.
        # Exact same syntax as PyTorch!
        loss = loss_fn(input_prompt)
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()
        
        print(vars(input_prompt))
        return input_prompt.value, loss.value