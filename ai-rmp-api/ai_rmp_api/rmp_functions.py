from typing import Dict, Any
import ratemyprofessor
import groq


def get_professor_info(school_name: str, professor_name: str) -> Dict[str, Any]:
    school = ratemyprofessor.get_school_by_name(school_name)
    if not school:
        return {"error": f"School '{school_name}' not found."}

    professors = ratemyprofessor.get_professors_by_school_and_name(
        school, professor_name
    )

    if not professors:
        return {
            "error": f"No professors found with the name '{professor_name}' at {school_name}."
        }

    # Assume the first result is the correct professor
    professor = professors[0]

    output = {
        "name": professor.name,
        "department": professor.department,
        "average_rating": round(professor.rating, 2),
        "difficulty_rating": round(professor.difficulty, 2),
        "would_take_again": round(professor.would_take_again, 2),
        "total_ratings": professor.num_ratings,
        "courses": [],
    }

    courses = {}
    for rating in professor.get_ratings():
        if rating.class_name not in courses:
            courses[rating.class_name] = []
        courses[rating.class_name].append(rating)

    for course, ratings in courses.items():
        course_info = {
            "name": course,
            "average_rating": round(sum(r.rating for r in ratings) / len(ratings), 2),
            "average_difficulty": round(
                sum(r.difficulty for r in ratings) / len(ratings), 2
            ),
            "number_of_ratings": len(ratings),
            "sample_comments": [r.comment for r in ratings if r.comment][:5],
        }
        output["courses"].append(course_info)

    return output


def check_school_exists(school_name: str) -> Dict[str, Any]:
    school = ratemyprofessor.get_school_by_name(school_name)
    if school:
        return {"exists": True, "name": school.name}
    return {"exists": False, "error": f"School '{school_name}' not found."}


def search_professors_by_name(professor_name: str, school_name: str) -> Dict[str, Any]:
    school = ratemyprofessor.get_school_by_name(school_name)
    professors = ratemyprofessor.get_professors_by_school_and_name(
        school, professor_name
    )
    return {"professors": [p.name for p in professors]}


def check_professor_exists(school_name: str, professor_name: str) -> Dict[str, Any]:
    school_result = check_school_exists(school_name)
    if not school_result["exists"]:
        return {"exists": False, "error": school_result["error"]}

    professors = ratemyprofessor.get_professors_by_school_and_name(
        ratemyprofessor.get_school_by_name(school_name), professor_name
    )
    if professors:
        return {"exists": True, "name": professors[0].name}
    return {
        "exists": False,
        "error": f"No professor found with the name '{professor_name}' at {school_name}.",
    }


def list_professor_classes(school_name: str, professor_name: str) -> Dict[str, Any]:
    professor_result = check_professor_exists(school_name, professor_name)
    if not professor_result["exists"]:
        return {"error": professor_result["error"]}

    professor = ratemyprofessor.get_professors_by_school_and_name(
        ratemyprofessor.get_school_by_name(school_name), professor_name
    )[0]
    classes = sorted(list(set(rating.class_name for rating in professor.get_ratings())))
    return {"classes": classes}


def get_full_school_name(school_name: str) -> Dict[str, Any]:
    try:
        client = groq.Groq()

        prompt = f"""Given the school name or acronym "{school_name}", 
        please provide the full, official name of the school. 
        If it's already the full name, just return it as is. 
        If you're not sure, please respond with "Unable to determine full school name."
        Respond with only the school name, nothing else."""

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.1,
            max_tokens=100,
            top_p=1,
            stop=None,
        )

        full_name = chat_completion.choices[0].message.content.strip()
        return {"full_name": full_name}
    except Exception as e:
        return {"error": f"Error getting full school name: {str(e)}"}
