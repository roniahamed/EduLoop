from django.contrib.sessions.middleware import SessionMiddleware


class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        session_key = request.headers.get('X-Session-Id')

        if session_key:
            request.session = self.SessionStore(session_key)
        else:
            super().process_request(request)