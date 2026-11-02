from supabase import create_client, Client
from classbridge import config


def get_anon_client() -> Client:
    """Used for login/signup. RLS applies."""
    return create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)


def get_user_client(access_token: str) -> Client:
    """Acts as the logged-in user, so RLS limits what they can see."""
    client = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)
    client.postgrest.auth(access_token)
    return client


def get_admin_client() -> Client:
    """Bypasses RLS. Backend use only (notifications, seeding)."""
    if not config.SUPABASE_SERVICE_KEY:
        raise RuntimeError("SUPABASE_SERVICE_KEY is not set")
    return create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY)