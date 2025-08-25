{% if cookiecutter.worker == "rq" -%}
from admin_utils import register_view
{% endif -%}
from django.contrib import admin
from django.contrib.admin import register
{%- if cookiecutter.worker == "rq" %}
from django_rq.stats_views import stats
{%- endif %}

from .models import {{ cookiecutter.django_model_name }}
{%- if cookiecutter.worker == "rq" %}

register_view(app_label="django_rq", model_name="RQ")(stats)
{%- endif %}


@register({{ cookiecutter.django_model_name }})
class {{ cookiecutter.django_model_name }}Admin(admin.ModelAdmin):
    pass
