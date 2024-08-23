from langchain.tools import StructuredTool
from ai_rmp_api.rmp_functions import (
    check_school_exists,
    check_professor_exists,
    list_professor_classes,
    get_professor_info,
    get_full_school_name,
    search_professors_by_name,
)

check_school_tool = StructuredTool.from_function(
    func=check_school_exists,
    name="check_school",
    description="Check if a school exists in the Rate My Professors database. Use the full school name, not acronyms.",
)

search_professors_by_name_tool = StructuredTool.from_function(
    func=search_professors_by_name,
    name="search_professors_by_name",
    description="Search for a professor by name and school in the Rate My Professors database. Use the full school name, not acronyms.",
)

check_professor_tool = StructuredTool.from_function(
    func=check_professor_exists,
    name="check_professor",
    description="Check if a professor exists at a given school in the Rate My Professors database. Use the full school name, not acronyms.",
)

list_classes_tool = StructuredTool.from_function(
    func=list_professor_classes,
    name="list_classes",
    description="List all classes taught by a professor at a given school. Use the full school name, not acronyms.",
)

professor_info_tool = StructuredTool.from_function(
    func=get_professor_info,
    name="professor_info",
    description="Get detailed information about a professor at a given school. Use the full school name, not acronyms.",
)

get_full_school_name_tool = StructuredTool.from_function(
    func=get_full_school_name,
    name="get_full_school_name",
    description="Get the full school name from a given school name or acronym using groqchat.",
)

tools = [
    check_school_tool,
    check_professor_tool,
    list_classes_tool,
    professor_info_tool,
    get_full_school_name_tool,
]
