# Check that public files are returned without auth
import pytest
import requests

BROWSE_FILE = "SA/BROWSE/S1A_EW_GRDM_1SDH_20190206T190846_20190206T190951_025813_02DF0B_781A.jpg"
OBJ_PREFIX_FILE = "SA/METADATA_GRD_HS_CH/browse/ALAV2A104483200-OORIRFU_000.png"


@pytest.mark.parametrize("method", ("get", "head"))
def test_public_images(urls, method):
    url = urls.join(BROWSE_FILE)
    r = requests.request(method, url)

    assert r.status_code == 200
    assert r.headers["Content-Type"] == "image/jpeg"


@pytest.mark.parametrize("method", ("get", "head"))
def test_check_public_obj_prefix(urls, method):
    url = urls.join(OBJ_PREFIX_FILE)
    r = requests.request(method, url)

    assert r.status_code == 200


@pytest.mark.parametrize("method", ("get", "head"))
def test_404_on_bad_request(urls, method):
    url = urls.join("bad", "url.ext")
    r = requests.request(method, url)

    assert r.status_code == 404


def test_bad_cookie_value_cause_URS_redirect(urls):
    url = urls.join(urls.METADATA_FILE)
    cookies = {
        "urs_user_id": "badusername",
        "urs_access_token": "blah"
    }

    r = requests.get(url, cookies=cookies, allow_redirects=False)

    assert r.is_redirect is True
    assert r.headers["Location"] is not None
    assert "oauth/authorize" in r.headers["Location"]


def test_head_private_data(urls):
    # All files are publically headable!
    # TODO(reweeden): Is this desired?
    url = urls.join("PRIVATE", "ACCESS", "testfile")

    r = requests.head(url, allow_redirects=True)

    assert r.status_code == 200
    assert r.headers["Content-Length"] == "37"
    assert r.headers["Content-Type"] == "binary/octet-stream"
