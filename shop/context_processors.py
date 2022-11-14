from config.models import Config


def own_settings(request) -> dict:
    our_conf = Config.load()
    return {
        'ADMIN_EMAIL': our_conf.contact_form_email,
    }
