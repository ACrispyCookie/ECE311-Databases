import os
import requests
from cryptography.fernet import Fernet
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from . import database_service as db_service
from json import JSONDecodeError


not_authenticated = JsonResponse({"error": "Not authenticated"}, safe=False)


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def department(request):
    fernet = Fernet(os.environ.get('FERNET_KEY'))
    jsessionid = fernet.decrypt(request.headers.get('x-jsessionid', None).encode()).decode()
    csrf_token = fernet.decrypt(request.headers.get('x-sis-csrf-token', None).encode()).decode()
    authenticated_user_id = check_authenticated(jsessionid, csrf_token)
    if authenticated_user_id is None:
        return not_authenticated
    return db_service.get_department(authenticated_user_id)


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def department_courses(request):
    # fernet = Fernet(os.environ.get('FERNET_KEY'))
    # jsessionid = fernet.decrypt(request.headers.get('x-jsessionid', None).encode()).decode()
    # csrf_token = fernet.decrypt(request.headers.get('x-sis-csrf-token', None).encode()).decode()
    jsessionid = request.headers.get('x-jsessionid', None)
    csrf_token = request.headers.get('x-sis-csrf-token', None)
    authenticated_user_id = check_authenticated(jsessionid, csrf_token)
    authenticated_user_id = check_authenticated(jsessionid, csrf_token)
    if authenticated_user_id is None:
        return not_authenticated
    courseTitle = request.GET.get("search", None)
    return db_service.get_courses(authenticated_user_id, courseTitle)


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def course(request, courseId):
    fernet = Fernet(os.environ.get('FERNET_KEY'))
    jsessionid = fernet.decrypt(request.headers.get('x-jsessionid', None).encode()).decode()
    csrf_token = fernet.decrypt(request.headers.get('x-sis-csrf-token', None).encode()).decode()
    authenticated_user_id = check_authenticated(jsessionid, csrf_token)
    if authenticated_user_id is None:
        return not_authenticated
    return db_service.get_course(authenticated_user_id, courseId)


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def course_categories(request, courseId):
    fernet = Fernet(os.environ.get('FERNET_KEY'))
    jsessionid = fernet.decrypt(request.headers.get('x-jsessionid', None).encode()).decode()
    csrf_token = fernet.decrypt(request.headers.get('x-sis-csrf-token', None).encode()).decode()
    authenticated_user_id = check_authenticated(jsessionid, csrf_token)
    if authenticated_user_id is None:
        return not_authenticated
    categoryTitle = request.GET.get("search", None)
    return db_service.get_categories(authenticated_user_id, courseId, categoryTitle)


@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def category_posts(request, courseId, categoryTitle):
    fernet = Fernet(os.environ.get('FERNET_KEY'))
    jsessionid = fernet.decrypt(request.headers.get('x-jsessionid', None).encode()).decode()
    csrf_token = fernet.decrypt(request.headers.get('x-sis-csrf-token', None).encode()).decode()
    authenticated_user_id = check_authenticated(jsessionid, csrf_token)
    if authenticated_user_id is None:
        return not_authenticated
    if request.method == "POST":
        data = request.body.dict()
        return JsonResponse(data, safe=False)
        url = data.get("url", None)
        title = data.get("title", None)
        if url is None or title is None:
            return HttpResponse(status=400)
        return HttpResponse(status=200) if db_service.create_post(url, title, authenticated_user_id, categoryTitle, courseId) else HttpResponse(status=403)
    postTitle = request.GET.get("search", None)
    return db_service.get_category_posts(authenticated_user_id, courseId, categoryTitle, postTitle)


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def user(request, userId):
    fernet = Fernet(os.environ.get('FERNET_KEY'))
    jsessionid = fernet.decrypt(request.headers.get('x-jsessionid', None).encode()).decode()
    csrf_token = fernet.decrypt(request.headers.get('x-sis-csrf-token', None).encode()).decode()
    authenticated_user_id = check_authenticated(jsessionid, csrf_token)
    if authenticated_user_id is None:
        return not_authenticated
    return db_service.get_user(authenticated_user_id, userId)


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def user_posts(request, userId):
    fernet = Fernet(os.environ.get('FERNET_KEY'))
    jsessionid = fernet.decrypt(request.headers.get('x-jsessionid', None).encode()).decode()
    csrf_token = fernet.decrypt(request.headers.get('x-sis-csrf-token', None).encode()).decode()
    authenticated_user_id = check_authenticated(jsessionid, csrf_token)
    if authenticated_user_id is None:
        return not_authenticated
    return db_service.get_user_posts(authenticated_user_id, userId)


@csrf_exempt
@require_http_methods(["GET", "OPTIONS", "POST"])
def post(request, postId=None):
    fernet = Fernet(os.environ.get('FERNET_KEY'))
    jsessionid = fernet.decrypt(request.headers.get('x-jsessionid', None).encode()).decode()
    csrf_token = fernet.decrypt(request.headers.get('x-sis-csrf-token', None).encode()).decode()
    authenticated_user_id = check_authenticated(jsessionid, csrf_token)
    if authenticated_user_id is None:
        return not_authenticated
    return db_service.get_post(authenticated_user_id, postId)


@csrf_exempt
@require_http_methods(["GET", "PUT", "OPTIONS"])
def post_reactions(request, postId):
    fernet = Fernet(os.environ.get('FERNET_KEY'))
    jsessionid = fernet.decrypt(request.headers.get('x-jsessionid', None).encode()).decode()
    csrf_token = fernet.decrypt(request.headers.get('x-sis-csrf-token', None).encode()).decode()
    authenticated_user_id = check_authenticated(jsessionid, csrf_token)
    if authenticated_user_id is None:
        return not_authenticated
    if request.method == "PUT":
        upvote_type = request.POST.get("type", None)
        if upvote_type == None:
            return HttpResponse(status=400)
        return HttpResponse(status=200) if db_service.create_reaction(upvote_type, authenticated_user_id, postId) else HttpResponse(status=403)
    return db_service.get_post_reactions(authenticated_user_id, postId, request.GET)


"""
Checks if the user is authenticated.

This is a placeholder function and should be replaced with an actual authentication check 
for your application (e.g., by checking session data, token, etc.).

Returns:
    str: The authenticated_user_id of the authenticated user or None if authentication failed
"""
def check_authenticated(cookie, csrf_token):
    if cookie is None or csrf_token is None:
        return None

    user_profile_request = requests.get('https://sis-web.uth.gr/api/person/profiles',
                     cookies={'JSESSIONID': cookie})

    try:
        profile = user_profile_request.json()
        if "studentProfiles" not in profile:
            return None
        user_profile = profile["studentProfiles"][0]
        authenticated_user_id = user_profile["id"]
        departmentCode = user_profile["departmentCode"]
        departmentTitle = user_profile["departmentTitle"]
        username = user_profile["username"]

        create_department_if_not_exists(cookie, csrf_token, departmentCode, departmentTitle)
        create_user_if_not_exists(authenticated_user_id, username, departmentCode)
        
        return authenticated_user_id
    except JSONDecodeError:
        return None

"""
Checks if a specific department exists in the database
and if it doesn't, it creates it.
"""
def create_department_if_not_exists(cookie, csrf_token, departmentCode, departmentTitle):
    department_exists_result = db_service.dictfetchall(db_service.execute_query("SELECT COUNT(*) as count FROM Departments WHERE departmentCode=%s", [departmentCode]))
    if department_exists_result[0]["count"] == 0:
        courses_request = requests.get('https://sis-web.uth.gr/feign/student/program_courses',
                        cookies={'JSESSIONID': cookie},
                        headers={'X-Csrf-Token': csrf_token}).json()
        db_service.create_department(departmentCode, departmentTitle, courses_request["programCourse"])

"""
Checks if a specific user exists in the database
and if it doesn't, it creates it.
"""
def create_user_if_not_exists(authenticated_user_id, username, departmentCode):
    user_exists_result = db_service.dictfetchall(db_service.execute_query("SELECT COUNT(*) as count FROM Users WHERE id=%s", [authenticated_user_id]))
    if user_exists_result[0]["count"] == 0:
        db_service.create_user(authenticated_user_id, username, departmentCode)


