from healthcheck import HealthCheck
from . import gene_blueprint

health = HealthCheck()


def api_available():
    return True, "Api running"


def application_data():
    return {"maintainer": "André de Sousa Araújo",
            "git_repo": "https://github.com/xpto"}


health.add_check(api_available)
health.add_section("application", application_data)

gene_blueprint.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
