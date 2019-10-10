import conneg_headers
import pprint


# ref https://w3c.github.io/dxwg/conneg-by-ap/#http-listprofiles
def normal_header():
    h = '''
          <http://example.org/resource/a>;
                  rel="self";
                  type="text/turtle";
                  profile="urn:example:profile:x",
          <http://example.org/resource/a>;
                  rel="alternate";
                  type="text/turtle";
                  profile="urn:example:profile:y",
          <http://example.org/resource/a>;
                  rel="alternate";
                  type="application/xml";
                  profile="urn:example:profile:x",
          <http://example.org/resource/a>;
                  rel="alternate";
                  type="application/xml";
                  profile="urn:example:profile:y",
          <http://example.org/resource/a>;
                  rel="alternate";
                  type="text/html"
          '''.replace(' ', '').replace('\n', '')

    lh = conneg_headers.LinkHeaderParser(h)
    assert lh.valid_list_profiles


def header_urn_with_comma():
    h = '''
        <http://example.org/resource/a>;
              rel="self";
              type="text/turtle";
              profile="urn:example:profile:x",
        <http://example.org/resource/a>;
              rel="alternate";
              type="text/turtle";
              profile="urn:example:profile,y"        
        '''.replace(' ', '').replace('\n', '')

    lh = conneg_headers.LinkHeaderParser(h)
    assert lh.valid_list_profiles


def header_urn_with_semicolon():
    h = '''
        <http://example.org/resource/a>;
              rel="self";
              type="text/turtle";
              profile="urn:example:profile:x",
        <http://example.org/resource/a>;
              rel="alternate";
              type="text/turtle";
              profile="urn:example:profile;y"
        '''.replace(' ', '').replace('\n', '')

    lh = conneg_headers.LinkHeaderParser(h)
    assert lh.valid_list_profiles


def header_uri_with_comma():
    h = '''
        <http://example.org/resource/a,a>;
              rel="self";
              type="text/turtle";
              profile="urn:example:profile:x",
        <http://example.org/resource/a,a>;
              rel="alternate";
              type="text/turtle";
              profile="urn:example:profile:y",
        <http://example.org/resource/a,a>;
              rel="alternate";
              type="text/turtle";
              profile="urn:example:profile,z"
        '''.replace(' ', '').replace('\n', '')

    lh = conneg_headers.LinkHeaderParser(h)
    assert lh.valid_list_profiles


def header_uri_with_two_self():
    h = '''
        <http://example.org/resource/a,a>;
              rel="self";
              type="text/turtle";
              profile="urn:example:profile:x",
        <http://example.org/resource/a,a>;
              rel="alternate";
              type="text/turtle";
              profile="urn:example:profile:y",
        <http://example.org/resource/a>;
              rel="self";
              type="application/xml";
              profile="urn:example:profile:x"
        '''.replace(' ', '').replace('\n', '')

    lh = conneg_headers.LinkHeaderParser(h)
    assert not lh.valid_list_profiles


# TODO: work out if this is valid or not
def header_uri_with_no_rel():
    h = '''
        <http://example.org/resource/a,a>;
              rel="self";
              type="text/turtle";
              profile="urn:example:profile:x",
        <http://example.org/resource/a,a>;
              rel="alternate";
              type="text/turtle";
              profile="urn:example:profile:y",
        <http://example.org/resource/a>;
              type="application/xml";
              profile="urn:example:profile:x"
        '''.replace(' ', '').replace('\n', '')

    lh = conneg_headers.LinkHeaderParser(h)
    assert lh.valid_list_profiles


# https://w3c.github.io/dxwg/conneg-by-ap/#getresourcebyprofile

if __name__ == '__main__':
    normal_header()
    header_urn_with_comma()
    header_urn_with_semicolon()
    header_uri_with_comma()
    header_uri_with_two_self()
    header_uri_with_no_rel()
