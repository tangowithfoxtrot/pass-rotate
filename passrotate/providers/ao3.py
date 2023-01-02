from passrotate.provider import Provider, ProviderOption, register_provider
from passrotate.forms import get_form
import requests

class Ao3(Provider):
    """
    [archiveofourown.org]
    login=me@example.com
    """
    name = "Archive of our Own"
    domains = [
        "archiveofourown.org",
    ]
    options = {
        "login": ProviderOption(str, "Your email or username")
    }

    def __init__(self, options):
        self.login = options["login"]

    def prepare(self, username, old_password):
        self._session = requests.Session()

        ###authenticate
        r = self._session.get("https://archiveofourown.org/users/login")
        form = get_form(r.text, id="new_user")
        form.update({
            "user[login]": self.login,
            "user[password]": old_password
            })
        r = self._session.post("https://archiveofourown.org/users/login", data=form)

        self.username = list(filter(None, str.split(r.url, "/")))[-1]

        ###load form
        r = self._session.get("https://archiveofourown.org/users/" + self.username + "/change_password")
        self._form = get_form(r.text, method="post")

    def execute(self, old_password, new_password):
        self._form.update({
            "password_check" : old_password,
            "password" : new_password,
            "password_confirmation" : new_password
            })
        r = self._session.post("https://archiveofourown.org/users/" + self.username + "/changed_password", data=self._form)

register_provider(Ao3)
