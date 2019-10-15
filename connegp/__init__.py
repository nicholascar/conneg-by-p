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
        i.e. Link: <http:/...>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"
        """

        links = []
        replace_chars = ' "'

        for val in re.split(', *<', link_header):
            try:
                url, params = val.split(';', 1)
            except ValueError:
                url, params = val, ''

            link = {
                'uri': url.strip('<> "')
            }

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
        self.profiles = []
        self.valid = False

        self._parse(accept_profile_header)
        self._is_valid()

    def _parse(self, link_header):
        """Return a dict of parsed link headers
        i.e. Link: <http:/.../front.jpeg>; q="0.9",<urn:one:two:three:y>; q=0.5
        """

        for val in re.split(', *<', link_header):
            try:
                uri, q = val.split(';', 1)
            except ValueError:
                uri, q = val, 'q=1'

            link = {
                'profile': uri.strip('<> "'),
                'q': float(q.split('=')[1])
            }

            self.profiles.append(link)
        self.profiles = sorted(self.profiles, key=lambda k: k['q'], reverse=True)

    def _is_valid(self):
        self.valid = True


class ProfileQsaParser:
    def __init__(self, profiles_qsa):
        self.profiles = []
        self.valid = False

        self._parse(profiles_qsa)

    def _parse(self, profiles_qsa):
        """Return a dict of parsed _ proxies Query String Argument
        i.e. _profile=<http://example.org/profile/x>; q="0.9",<urn:one:two:three:y>; q=0.5
        """

        # split on comma, but not if comma within < >
        within = False
        splits = []
        for i, letter in enumerate(profiles_qsa):
            if letter == '<':
                within = True
            elif letter == '>':
                within = False
            elif letter == ',' and within is False:
                splits.append(i)
            else:
                pass

        profiles = []
        start = 0
        for i, split in enumerate(splits):
            profiles.append(profiles_qsa[start:split])
            start = splits[i] + 1

        profiles.append(profiles_qsa[start:])

        for i, profile in enumerate(profiles):
            # if the profile ID is a URI (HTTP URI or a URN) then it must be enclosed in <>
            if 'http:' in profile or 'https:' in profile or 'urn:' in profile:
                if not profile.startswith('<') and '>' not in profile:
                    self.valid = False
                    return None
            try:
                p, q = profile.split(';', 1)
            except ValueError:
                p, q = profile, 'q=1'

            profile = {
                'profile': profile,
                'q': float(q.split('=')[1])
            }

            self.profiles.append(profile)
        self.profiles = sorted(self.profiles, key=lambda k: k['q'], reverse=True)

        self.valid = True
