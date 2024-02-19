from rest_framework.response import Response


def validation_error_resp(error):
    resp = {
        "errors": {
            "error": "Invalid Input",
            "field_errors": error.detail
        }
    }
    return resp

def business_error_resp(error):
    resp = {
        "errors": {
            "error": error.message
        }
    }
    return resp