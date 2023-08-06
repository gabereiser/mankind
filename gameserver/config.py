import os


class Configuration:
    debug: bool = os.environ.get("DEBUG", True)
    secret_key: str = os.environ.get("SECRET_KEY", "changeme")
    domain: str = os.environ.get("DOMAIN", "localhost")
    port: int = os.environ.get("PORT", 8080)
    godaddy_key: str | None = os.environ.get("GODADDY_KEY", "")
    godaddy_secret: str | None = os.environ.get("GODADDY_SECRET", "")
    aws_key: str | None = os.environ.get("AWS_ACCESS_KEY", "")
    aws_secret: str | None = os.environ.get("AWS_SECRET_KEY", "")
    db_url: str = os.environ.get("DB_URL", "localhost:5432/exodb")
    db_user: str = os.environ.get("DB_USER", "postgres")
    db_pass: str = os.environ.get("DB_PASS", "postgres")


_c = Configuration()


def get_config() -> Configuration:
    return _c
