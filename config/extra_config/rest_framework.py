REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    #"DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    #"DEFAULT_PAGINATION_CLASS": "core.pagination.Pagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
       "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
