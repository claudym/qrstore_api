import os
import json
from app import server


# UTILS
def post_token():
    data = {
        "email": os.environ.get("QR_EMAIL"),
        "password": os.environ.get("QR_PASSWORD"),
    }
    response = server.test_client().post("/token", json=data)
    res = json.loads(response.data.decode("utf-8"))
    return res


# TESTS
# user
def test_get_user_missing_auth_header():
    response = server.test_client().get("/user/leorio")
    res = json.loads(response.data.decode("utf-8"))
    assert res.get("message") == "Missing Authorization Header"


def test_get_user():
    access_token = post_token().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = server.test_client().get("/user/leorio", headers=headers)
    res = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert type(res.get("id")) == int
    assert type(res.get("role_id")) == int
    assert type(res.get("username")) == str
    assert (
        type(res.get("first_name")) == type(None) or type(res.get("first_name")) == str
    )
    assert type(res.get("last_name")) == type(None) or type(res.get("last_name")) == str
    assert type(res.get("tax_id")) == type(None) or type(res.get("tax_id")) == str
    assert type(res.get("photo_url")) == type(None) or type(res.get("photo_url")) == str


def test_get_me():
    access_token = post_token().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = server.test_client().get("/me", headers=headers)
    res = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert type(res.get("id")) == int
    assert type(res.get("role_id")) == int
    assert type(res.get("username")) == str
    assert (
        type(res.get("first_name")) == type(None) or type(res.get("first_name")) == str
    )
    assert type(res.get("last_name")) == type(None) or type(res.get("last_name")) == str
    assert type(res.get("tax_id")) == type(None) or type(res.get("tax_id")) == str
    assert type(res.get("photo_url")) == type(None) or type(res.get("photo_url")) == str


if __name__ == "__main__":
    # test_get_user_missing_auth_header()
    # test_get_user()
    pass
