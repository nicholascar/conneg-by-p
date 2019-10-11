import re


class LinkHeaderParser:
    def __init__(self, link_header):
        self.link_headers = []
        self.profiles = {}
        self.valid_list_profiles = False
        self.valid_profile_tokens = False

        self._parse(link_header)
        self._get_profiles()
        self._is_valid_list_profiles()
        self._is_valid_profile_tokens()

    # from Requests:
    # https://github.com/psf/requests/blob/f5dacf84468ab7e0631cc61a3f1431a32e3e143c/requests/utils.py#L580
    def _parse(self, link_header):
        """Return a dict of parsed link headers proxies.
        i.e. Link: <http:/.../front.jpeg>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"
        """

        links = []
        replace_chars = ' "'

        for val in re.split(', *<', link_header):
            try:
                url, params = val.split(';', 1)
            except ValueError:
                url, params = val, ''

            link = {}
            link['uri'] = url.strip('<> "')

            for param in params.split(';'):
                try:
                    key, value = param.split('=')
                except ValueError:
                    break

                link[key.strip(replace_chars)] = value.strip(replace_chars)

            links.append(link)

        self.link_headers = links

    def _get_profiles(self):
        # profiles
        for l in self.link_headers:
            if l['uri'] == 'http://www.w3.org/ns/dx/prof/Profile':  # all Link header lines have a 'uri'
                if l.get('anchor') and l.get('token'):
                    self.profiles[l['anchor']] = l['token']

    def _is_valid_list_profiles(self):
        # Each list profiles set of Link headers must indicate only one rel="self"
        rel_self = 0
        for link in self.link_headers:
            if link.get('rel') == 'self':
                rel_self += 1
        if rel_self == 1:
            self.valid_list_profiles = True

    def _is_valid_profile_tokens(self):
        return True


class AcceptProfileHeaderParser:
    def __init__(self, accept_profile_header):
        self.accept_profiles = []
        self.valid = False

        self._parse(accept_profile_header)
        self._is_valid()

    def _parse(self, link_header):
        """Return a dict of parsed link headers proxies.
        i.e. Link: <http:/.../front.jpeg>; q="0.9",<urn:one:two:three:y>; q=0.5
        """

        for val in re.split(', *<', link_header):
            try:
                uri, q = val.split(';', 1)
            except ValueError:
                uri, q = val, 'q=1'

            link = {
                'uri': uri.strip('<> "'),
                'q': float(q.split('=')[1])
            }

            self.accept_profiles.append(link)
        self.accept_profiles = sorted(self.accept_profiles, key=lambda k: k['q'], reverse=True)

    def _is_valid(self):
        self.valid = True
