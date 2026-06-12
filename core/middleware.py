import hashlib
from datetime import timedelta
from django.utils import timezone
from user_agents import parse
from .models import Visitor

class VisitorTrackingMiddleware:
    EXCLUDED_PATHS = (
        "anything-but-aninda-admin/",
        "anything-but-aninda-admin/core/visitor/",
        "admin/",
        "/static/",
        "/media/",
        "/favicon.ico",
    )
    
    VISIT_TIMEOUT_MINUTES = 30
    
    def __init__(self, get_response ):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path.startswith(self.EXCLUDED_PATHS):
            return response
        
        if not request.session.session_key:
            request.session.create()
        
        session_key = (request.session.session_key)
        
        ip_address = (
            self.get_client_ip(request)
        )
        
        user_agent_string = (
            request.META.get(
                "HTTP_USER_AGENT",
            )
        )
        
        ua = parse( user_agent_string )
        
        fingerprint = (
            self.generate_fingerprint(
                ip_address,
                user_agent_string,
                session_key 
            )
        )
        
        cutoff = ( timezone.now() - timedelta( minutes=self.VISIT_TIMEOUT_MINUTES))
        
        visitor = (
            Visitor.objects.filter(
                fingerprint = fingerprint,
                path = request.path,
                last_visit__gte = cutoff
                ).first()
        )
        
        if visitor:
            visitor.visit_count += 1
            visitor.save(
                update_fields = [
                    "visit_count",
                    "last_visit"
                ]
            )
        else:
            Visitor.objects.update_or_create(
                fingerprint = fingerprint,
                session_key = session_key,
                ip_address = ip_address,
                browser = ua.browser,
                browser_version = ua.browser.version_string,
                os_name = ua.os.family,
                os_version = ua.os.version_string,
                device_name = ua.device.family,
                is_mobile = ua.is_mobile,
                is_tablet = ua.is_tablet,
                is_pc = ua.is_pc,
                is_bot = ua.is_bot,
                path = request.path,
                referrer = request.META.get("HTTP_REFERRER"),
                user_agent = user_agent_string
            )
        return response
    
    def generate_fingerprint( self, ip, user_agent, session_key ):
        raw = (
            f"{ip}"
            f"{user_agent}"
            f"{session_key}"
        )
        return hashlib.sha256(raw.encode()).hexdigest()
    
    def get_client_ip ( self, request ):
        x_forwarded_for = (request.META.get("HTTP_X_FORWARDED_FOR"))
        
        if x_forwarded_for:
            return(x_forwarded_for.split(",")[0].strip())
        
        return request.META.get("REMOTE_ADDR")