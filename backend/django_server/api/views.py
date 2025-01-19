from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from . import database_service as db_service
from json import JSONDecodeError
import requests


not_authenticated = JsonResponse({"error": "Not authenticated"}, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def department(request):
    jsessionid = request.headers.get('x-jsessionid', None)
    csrf_token = request.headers.get('x-sis-csrf-token', None)
    user_id = check_authenticated(jsessionid, csrf_token)
    if user_id is None:
        return not_authenticated
    return db_service.get_department(user_id)


@csrf_exempt
@require_http_methods(["GET"])
def department_courses(request):
    jsessionid = request.headers.get('x-jsessionid', None)
    csrf_token = request.headers.get('x-sis-csrf-token', None)
    user_id = check_authenticated(jsessionid, csrf_token)
    if user_id is None:
        return not_authenticated
    return db_service.get_courses(user_id)


@csrf_exempt
@require_http_methods(["GET"])
def course(request, courseId):
    jsessionid = request.headers.get('x-jsessionid', None)
    csrf_token = request.headers.get('x-sis-csrf-token', None)
    user_id = check_authenticated(jsessionid, csrf_token)
    if user_id is None:
        return not_authenticated
    return db_service.get_course(courseId)


@csrf_exempt
@require_http_methods(["GET"])
def course_categories(request, courseId):
    jsessionid = request.headers.get('x-jsessionid', None)
    csrf_token = request.headers.get('x-sis-csrf-token', None)
    user_id = check_authenticated(jsessionid, csrf_token)
    if user_id is None:
        return not_authenticated
    return db_service.get_categories(courseId)


@csrf_exempt
@require_http_methods(["GET"])
def category_posts(request, courseId, titleId):
    jsessionid = request.headers.get('x-jsessionid', None)
    csrf_token = request.headers.get('x-sis-csrf-token', None)
    user_id = check_authenticated(jsessionid, csrf_token)
    if user_id is None:
        return not_authenticated
    return db_service.get_category_posts(courseId, titleId)


@csrf_exempt
@require_http_methods(["GET"])
def user(request, userId):
    jsessionid = request.headers.get('x-jsessionid', None)
    csrf_token = request.headers.get('x-sis-csrf-token', None)
    user_id = check_authenticated(jsessionid, csrf_token)
    if user_id is None:
        return not_authenticated
    return db_service.get_user(userId)


@csrf_exempt
@require_http_methods(["GET"])
def user_posts(request, userId):
    jsessionid = request.headers.get('x-jsessionid', None)
    csrf_token = request.headers.get('x-sis-csrf-token', None)
    user_id = check_authenticated(jsessionid, csrf_token)
    if user_id is None:
        return not_authenticated
    return db_service.get_user_posts(userId)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def post(request, postId=None):
    jsessionid = request.headers.get('x-jsessionid', None)
    csrf_token = request.headers.get('x-sis-csrf-token', None)
    user_id = check_authenticated(jsessionid, csrf_token)
    if request.method == "POST":
        return JsonResponse()
    elif user_id is None:
        return not_authenticated
    return db_service.get_post(postId)


@csrf_exempt
@require_http_methods(["GET"])
def post_reactions(request, postId):
    jsessionid = request.headers.get('x-jsessionid', None)
    csrf_token = request.headers.get('x-sis-csrf-token', None)
    user_id = check_authenticated(jsessionid, csrf_token)
    if user_id is None:
        return not_authenticated
    return db_service.get_post_reactions(postId, request.GET)


"""
Checks if the user is authenticated.

This is a placeholder function and should be replaced with an actual authentication check 
for your application (e.g., by checking session data, token, etc.).

Returns:
    str: The userId of the authenticated user or None if authentication failed
"""
def check_authenticated(cookie, csrf_token):
    if cookie is None or csrf_token is None:
        return None
    user_profile_request = requests.get('https://sis-web.uth.gr/api/person/profiles',
                     cookies={'x-jsessionid': cookie},
                     headers={'x-sis-csrf-token': csrf_token})
    
    try:
        profile = user_profile_request.json()
        if "studentProfiles" not in profile:
            return None
        user_profile = profile["studentProfiles"][0]
        user_id = user_profile["id"]
        departmentCode = user_profile["departmentCode"]

        department_exists_result = db_service.dictfetchall(db_service.execute_query("SELECT COUNT(*) as count FROM Departments WHERE departmentCode=%s", [departmentCode]))
        if department_exists_result[0]["count"] == 0:
            courses_request = requests.get('https://sis-web.uth.gr/feign/student/program_courses',
                            cookies={'x-jsessionid': cookie},
                            headers={'x-sis-csrf-token': csrf_token}).json()
            departmentTitle = user_profile["departmentTitle"]
            db_service.create_department(departmentCode, departmentTitle, courses_request["programCourse"])

        user_exists_result = db_service.dictfetchall(db_service.execute_query("SELECT COUNT(*) as count FROM Users WHERE id=%s", [user_id]))
        if user_exists_result[0]["count"] == 0:
            username = user_profile["username"]
            db_service.create_user(user_id, username, departmentCode)
        
        return user_id
    except JSONDecodeError:
        return None

