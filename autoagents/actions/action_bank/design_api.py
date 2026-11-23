#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@From    : https://github.com/geekan/MetaGPT/blob/main/metagpt/actions/design_api.py
"""
import shutil
from pathlib import Path
from typing import List

from autoagents.actions import Action, ActionOutput
from autoagents.system.const import WORKSPACE_ROOT
from autoagents.system.logs import logger
from autoagents.system.utils.common import CodeParser
from autoagents.system.utils.mermaid import mermaid_to_file

PROMPT_TEMPLATE = """
# Context
{context}

## Format example
{format_example}
-----
Role: You are an architect; the goal is to design a SOTA PEP8-compliant python system; make the best use of good open source tools
Requirement: Fill in the following missing information based on the context, note that all sections are response with code form separately
Max Output: 8192 chars or 2048 tokens. Try to use them up.
Attention: Use '##' to split sections, not '#', and '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote.

## Implementation approach: Provide as Plain text. Analyze the difficult points of the requirements, select the appropriate open-source framework.

## Python package name: Provide as Python str with python triple quoto, concise and clear, characters only use a combination of all lowercase and underscores

## File list: Provided as Python list[str], the list of ONLY REQUIRED files needed to write the program(LESS IS MORE!). Only need relative paths, comply with PEP8 standards. ALWAYS write a main.py or app.py here

## Data structures and interface definitions: Use mermaid classDiagram code syntax, including classes (INCLUDING __init__ method) and functions (with type annotations), CLEARLY MARK the RELATIONSHIPS between classes, and comply with PEP8 standards. The data structures SHOULD BE VERY DETAILED and the API should be comprehensive with a complete design. 

## Program call flow: Use sequenceDiagram code syntax, COMPLETE and VERY DETAILED, using CLASSES AND API DEFINED ABOVE accurately, covering the CRUD AND INIT of each object, SYNTAX MUST BE CORRECT.

## Anything UNCLEAR: Provide as Plain text. Make clear here.

"""
FORMAT_EXAMPLE = """
---
## Implementation approach
We will ...

## Python package name
```python
"snake_game"
```

## File list
```python
[
    "main.py",
]
```

## Data structures and interface definitions
```mermaid
classDiagram
    class Game{
        +int score
    }
    ...
    Game "1" -- "1" Food: has
```

## Program call flow
```mermaid
sequenceDiagram
    participant M as Main
    ...
    G->>M: end game
```

## Anything UNCLEAR
The requirement is clear to me.
---
"""
OUTPUT_MAPPING = {
    "Implementation approach": (str, ...),
    "Python package name": (str, ...),
    "File list": (List[str], ...),
    "Data structures and interface definitions": (str, ...),
    "Program call flow": (str, ...),
    "Anything UNCLEAR": (str, ...),
}


class WriteDesign(Action):
    def __init__(self, name="WriteDesign", context=None, llm=None):
        super().__init__(name, context, llm)
        self.desc = "Based on the PRD, think about the system design, and design the corresponding APIs, data structures, and work flow."

    async def run(self, context):
        prompt = PROMPT_TEMPLATE.format(context=context, format_example=FORMAT_EXAMPLE)
        rsp = await self.llm.aask(prompt)
        
        parsed_data = CodeParser.parse_code(block=True, text=rsp)
        
        return ActionOutput(content=rsp, instruct_content=parsed_data)