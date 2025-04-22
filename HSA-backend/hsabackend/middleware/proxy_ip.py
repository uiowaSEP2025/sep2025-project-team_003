def reverse_proxy(get_response):
    def middleware(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
            request.META['REMOTE_ADDR'] = ip
        return get_response(request)
    return middleware
