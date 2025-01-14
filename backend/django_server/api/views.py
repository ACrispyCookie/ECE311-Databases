from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction, connection
import json

"""
Return all rows from a cursor as a dict.
Assume the column names are unique.
"""
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

"""
Execute a query and return the cursor.
"""
def execute_query(query, params=None):
    with transaction.atomic():
        cursor = connection.cursor()
        cursor.execute(query, params)
        return cursor

"""
Checks if the user is authenticated
"""
def authenticated():
    return True

"""
Handles a simple GET request that runs an SQL query
and retrieves a result set
"""
def get_request(query, params, check_auth=True, empty_response=None):
    if check_auth and not authenticated():
        return JsonResponse({"error": "Not authenticated"}, safe=False)
    
    result = dictfetchall(execute_query(query, params))

    if empty_response is not None and len(result) == 0:
        return empty_response
    return JsonResponse(result, safe=False)
    
@require_http_methods(["GET"])
def department(request, departmentCode=None):
    if departmentCode == None:
        query = "SELECT * FROM Departments;"
        params = []
        check_auth = True
        return get_request(query, params, check_auth)
    else:
        query = "SELECT * FROM Departments WHERE departmentCode = %s;"
        params = [departmentCode]
        check_auth = True
        empty_response = JsonResponse({"error": "Department not found"}, safe=False)
        return get_request(query, params, check_auth, empty_response)

@require_http_methods(["GET"])
def department_courses(request, departmentCode):
    query = "SELECT * FROM Courses WHERE departmentCode = %s;"
    params = [departmentCode]
    check_auth = True
    return get_request(query, params, check_auth)
    
@require_http_methods(["GET"])
def course(request, courseId):
    query = "SELECT * FROM Courses WHERE courseId = %s;"
    params = [courseId]
    check_auth = True
    empty_response = JsonResponse({"error": "Course not found"}, safe=False)
    return get_request(query, params, check_auth, empty_response)
    
@require_http_methods(["GET"])
def course_categories(request, courseId):
    query = "SELECT * FROM Categories WHERE courseId = %s;"
    params = [courseId]
    check_auth = True
    return get_request(query, params, check_auth)

@require_http_methods(["GET"])
def category_posts(request, courseId, titleId):
    query = "SELECT * FROM Posts WHERE courseId = %s AND titleId = %s;"
    params = [courseId, titleId]
    check_auth = True
    return get_request(query, params, check_auth)

@require_http_methods(["GET"])
def user(request, userId):
    query = "SELECT * FROM Users WHERE id = %s;"
    params = [userId]
    check_auth = True
    empty_response = JsonResponse({"error": "User not found"}, safe=False)
    return get_request(query, params, check_auth, empty_response)

@require_http_methods(["GET"])
def user_posts(request, userId):
    query = "SELECT * FROM Posts WHERE userId = %s;"
    params = [userId]
    check_auth = True
    return get_request(query, params, check_auth)

@require_http_methods(["GET"])
def post(request, postId):
    query = "SELECT * FROM Posts WHERE id = %s;"
    params = [postId]
    check_auth = True
    empty_response = JsonResponse({"error": "Post not found"}, safe=False)
    return get_request(query, params, check_auth, empty_response)

@require_http_methods(["GET"])
def post_reactions(request, postId):
    if "type" not in request.GET or request.GET["type"] not in ["0", "1"]:
        return JsonResponse({"error": "Invalid request"}, safe=False)

    type_name = "upvotes" if request.GET["type"] == "1" else "downvotes" 
    is_count = "count" in request.GET and request.GET["count"].lower() == "true"

    if is_count:
        query = "SELECT COUNT(postId) as " + type_name + " FROM Reactions WHERE postId = %s AND upvote = %s;"
    else:
        query = "SELECT * FROM Reactions WHERE postId = %s AND upvote = %s;"
    params = [postId, request.GET["type"]]
    check_auth = True
    return get_request(query, params, check_auth)
