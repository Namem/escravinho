from django.contrib.auth.decorators import user_passes_test

def analista_required(view_func):
    return user_passes_test(lambda u: u.groups.filter(name='Analista').exists())(view_func)
