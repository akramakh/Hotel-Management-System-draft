
from rest_framework.views import exception_handler



def student_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['detail'] = 'This Proccess is Allowed for Admin Users Only'
        response.data['code'] = 'admin_allowed_only'
        response.data['messages'] = ''
        print(exc.detail)
    return response
