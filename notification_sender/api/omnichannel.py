from flask import make_response


def send(body):
    text = body.get('text')

    return make_response(
        {
            "message": f"{text}. Send ok!",
            "error": False
         }, 200
    )