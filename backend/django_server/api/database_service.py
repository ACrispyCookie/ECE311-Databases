from django.http import HttpResponse, JsonResponse
from django.db import transaction, connection

def get_department(userId):
    query = "SELECT * FROM Departments WHERE departmentCode = (SELECT departmentCode FROM Users WHERE id=%s);"
    params = [userId]
    empty_response = JsonResponse({"error": "Department not found"}, safe=False)
    return get_public_request(query, params, empty_response)

def get_courses(userId):
    query = "SELECT * FROM Courses WHERE departmentCode = (SELECT departmentCode FROM Users WHERE id=%s);"
    params = [userId]
    return get_public_request(query, params)

def get_course(userId, courseId):
    query = "SELECT * FROM Courses WHERE courseId = %s;"
    params = [courseId]
    permission_query = "SELECT id FROM Users as u INNER JOIN Courses as c ON u.departmentCode=c.departmentCode WHERE u.id=%s AND c.courseId=%s"
    permission_params = [userId, courseId]
    empty_response = JsonResponse({"error": "Course not found"}, safe=False)
    return get_permission_request(query, params, permission_query, permission_params, empty_response)

def get_categories(userId, courseId):
    query = "SELECT * FROM Categories WHERE courseId = %s;"
    params = [courseId]
    permission_query = "SELECT id FROM Users as u INNER JOIN Courses as c ON u.departmentCode=c.departmentCode WHERE u.id=%s AND c.courseId=%s"
    permission_params = [userId, courseId]
    return get_permission_request(query, params, permission_query, permission_params, empty_response)

def get_category_posts(userId, courseId, titleId):
    query = "SELECT * FROM Posts WHERE courseId = %s AND titleId = %s;"
    params = [courseId, titleId]
    permission_query = "SELECT id FROM Users as u INNER JOIN Courses as c ON u.departmentCode=c.departmentCode WHERE u.id=%s AND c.courseId=%s"
    permission_params = [userId, courseId]
    return get_permission_request(query, params, permission_query, permission_params, empty_response)

def get_user(userId, user_to_find):
    query = "SELECT * FROM Users WHERE id = %s;"
    params = [user_to_find]
    permission_query = "SELECT id FROM Users WHERE id=%s AND departmentCode IN (SELECT departmentCode FROM Users WHERE id=%s);"
    permission_params = [userId, user_to_find]
    empty_response = JsonResponse({"error": "User not found"}, safe=False)
    return get_permission_request(query, params, permission_query, permission_params, empty_response)

def get_user_posts(userId, user_to_find):
    query = "SELECT * FROM Posts WHERE userId = %s;"
    params = [user_to_find]
    permission_query = "SELECT id FROM Users WHERE id=%s AND departmentCode IN (SELECT departmentCode FROM Users WHERE id=%s);"
    permission_params = [userId, user_to_find]
    return get_permission_request(query, params, permission_query, permission_params)

def get_post(userId, postId):
    query = "SELECT * FROM Posts WHERE id = %s;"
    params = [postId]
    permission_query = "SELECT u.id FROM Users as u INNER JOIN Courses as c ON u.departmentCode=c.departmentCode INNER JOIN Posts as p ON p.courseId=c.courseId WHERE u.id=%s AND p.id=%s"
    permission_params = [userId, postId]
    empty_response = JsonResponse({"error": "Post not found"}, safe=False)
    return get_permission_request(query, params, permission_query, permission_params, empty_response)

def get_post_reactions(userId, postId, params):
    if "type" not in params or params["type"] not in ["0", "1"]:
        return JsonResponse({"error": "Invalid request"}, safe=False)
    type_name = "upvotes" if params["type"] == "1" else "downvotes" 
    is_count = "count" in params and params["count"].lower() == "true"

    if is_count:
        query = "SELECT COUNT(postId) as " + type_name + " FROM Reactions WHERE postId = %s AND upvote = %s;"
    else:
        query = "SELECT * FROM Reactions WHERE postId = %s AND upvote = %s;"
    params = [postId, params["type"]]
    permission_query = "SELECT u.id FROM Users as u INNER JOIN Courses as c ON u.departmentCode=c.departmentCode INNER JOIN Posts as p ON p.courseId=c.courseId WHERE u.id=%s AND p.id=%s"
    permission_params = [userId, postId]
    return get_permission_request(query, params, permission_query, permission_params)

def create_department(departmentCode, departmentTitle, courses):
    execute_query("INSERT INTO Departments (departmentTitle, departmentCode) VALUES (%s, %s)", [departmentTitle, departmentCode])
    for course in courses:
        create_course(course["title"], course["courseCode"], course["id"], departmentCode);

def create_course(courseTitle, courseCode, courseId, departmentCode):
    execute_query("INSERT INTO Courses (courseTitle, courseCode, courseId, departmentCode) VALUES (%s, %s, %s, %s)", [courseTitle, courseCode, courseId, departmentCode])

def create_category(categoryTitle, courseId):
    execute_query("INSERT INTO Categories (categoryTitle, courseId) VALUES (%s, %s)", [categoryTitle, courseId])

def create_user(userId, username, departmentCode):
    execute_query("INSERT INTO Users (username, id, departmentCode) VALUES (%s, %s, %s)", [username, userId, departmentCode])

def create_post(url, title, userId, titleId, courseId):
    pass

def create_reaction(upvote, userId, postId):
    pass

"""
Handles a simple GET request by executing a SQL query and returning the results as a JSON response.

This function checks for the presence of a permission query, and if provided, it verifies 
whether the user has the required permission. If no permission is found, it returns an error 
response. After that, it executes the main query, processes the results, and returns them as 
a JSON response. If no results are found and an `empty_response` is provided, it will return that.

Parameters:
    query (str): The SQL query to execute.
    params (tuple): The parameters to pass to the SQL query.
    permission_query (str, optional): The SQL query to check for permissions (default is None).
    permission_params (tuple, optional): The parameters to pass with the permission query (default is None).
    empty_response (JsonResponse, optional): The response to return when no results are found (default is None).

Returns:
    JsonResponse: A JSON response with the result of the query or an error message if permission is denied.
"""
def get_request(query, params, permission_query=None, permission_params=None, empty_response=None):
    if permission_query:
        has_permission = execute_query(permission_query, permission_params).fetchone() is not None
        if not has_permission:
            return JsonResponse({"error": "No permission"}, safe=False)

    result = dictfetchall(execute_query(query, params))
    if empty_response is not None and len(result) == 0:
        return empty_response
    return JsonResponse(result, safe=False)

"""
Wrapper function for a simple GET request that does not require permission checks.

This function calls `get_request` without a permission query, making it suitable 
for cases where no permission check is needed (e.g., public data).

Parameters:
    query (str): The SQL query to execute.
    params (tuple): The parameters to pass to the SQL query.
    empty_response (JsonResponse, optional): The response to return if no results are found (default is None).

Returns:
    JsonResponse: A JSON response with the result of the query or the empty_response if no results are found.
"""
def get_public_request(query, params, empty_response=None):
    return get_request(query, params, None, None, empty_response)

"""
Wrapper function for a GET request that includes permission checks.

This function calls `get_request` with the provided permission query and parameters 
to check if the user has permission before proceeding with the main query.

Parameters:
    query (str): The SQL query to execute.
    params (tuple): The parameters to pass to the SQL query.
    permission_query (str): The SQL query to check for permissions.
    permission_params (tuple): The parameters to pass with the permission query.
    empty_response (JsonResponse, optional): The response to return if no results are found (default is None).

Returns:
    JsonResponse: A JSON response with the result of the query or an error message if permission is denied.
"""
def get_permission_request(query, params, permission_query, permission_params, empty_response=None):
    return get_request(query, params, permission_query, permission_params, empty_response)

"""
Fetches all rows from a database cursor and returns them as a list of dictionaries.

This function processes the results of a SQL query, converting each row into a dictionary
where the column names are used as the keys and the row values are the values.

Parameters:
    cursor (Cursor): The database cursor containing the result set of an executed query.

Returns:
    list of dict: A list of dictionaries where each dictionary represents a row from the query result.
"""
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

"""
Executes a SQL query with the provided parameters and returns the cursor.

This function executes a query using the given SQL string and parameters, ensuring the query
is run inside a transaction. It returns the cursor, which can be used to fetch the results.

Parameters:
    query (str): The SQL query to execute.
    params (tuple, optional): The parameters to pass with the query (default is None).

Returns:
    Cursor: The cursor object used to fetch the results of the query.
"""
def execute_query(query, params=None):
    with transaction.atomic():
        cursor = connection.cursor()
        cursor.execute(query, params)
        return cursor