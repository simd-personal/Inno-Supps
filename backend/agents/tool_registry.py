"""
Tool registry for agent runtime
"""

import json
from typing import Dict, Any, Callable, List
from pydantic import BaseModel, Field
import inspect

class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None

class ToolSchema(BaseModel):
    name: str
    description: str
    parameters: List[ToolParameter]
    returns: str

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.schemas: Dict[str, ToolSchema] = {}
    
    def register(self, func: Callable) -> None:
        """Register a function as a tool"""
        tool_name = func.__name__
        self.tools[tool_name] = func
        
        # Generate schema from function signature
        sig = inspect.signature(func)
        parameters = []
        
        for param_name, param in sig.parameters.items():
            param_type = "string"
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list:
                    param_type = "array"
                elif param.annotation == dict:
                    param_type = "object"
            
            parameters.append(ToolParameter(
                name=param_name,
                type=param_type,
                description=param.__doc__ or f"Parameter {param_name}",
                required=param.default == inspect.Parameter.empty,
                default=param.default if param.default != inspect.Parameter.empty else None
            ))
        
        # Get return type
        return_type = "string"
        if hasattr(func, '__annotations__') and 'return' in func.__annotations__:
            return_annotation = func.__annotations__['return']
            if return_annotation == int:
                return_type = "integer"
            elif return_annotation == float:
                return_type = "number"
            elif return_annotation == bool:
                return_type = "boolean"
            elif return_annotation == list:
                return_type = "array"
            elif return_annotation == dict:
                return_type = "object"
        
        self.schemas[tool_name] = ToolSchema(
            name=tool_name,
            description=func.__doc__ or f"Tool {tool_name}",
            parameters=parameters,
            returns=return_type
        )
    
    def get_tool(self, name: str) -> Callable:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def get_schema(self, name: str) -> ToolSchema:
        """Get tool schema by name"""
        return self.schemas.get(name)
    
    def list_tools(self) -> List[str]:
        """List all registered tool names"""
        return list(self.tools.keys())
    
    def list_schemas(self) -> List[ToolSchema]:
        """List all tool schemas"""
        return list(self.schemas.values())
    
    def validate_call(self, name: str, args: Dict[str, Any]) -> bool:
        """Validate tool call arguments"""
        if name not in self.tools:
            return False
        
        schema = self.schemas[name]
        for param in schema.parameters:
            if param.required and param.name not in args:
                return False
        
        return True
    
    def call_tool(self, name: str, args: Dict[str, Any]) -> Any:
        """Call a tool with arguments"""
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")
        
        if not self.validate_call(name, args):
            raise ValueError(f"Invalid arguments for tool {name}")
        
        tool = self.tools[name]
        return tool(**args)

# Global tool registry
tool_registry = ToolRegistry()
