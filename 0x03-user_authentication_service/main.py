#!/usr/bin/env python3
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 201, f"Failed to register user: {response.text}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with a wrong password."""
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401, f"Unexpected status code: {response.status_code}. Response: {response.text}"


def log_in(email: str, password: str) -> str:
    """Log in with valid credentials and return the session ID."""
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200, f"Failed to log in: {response.text}"
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Access the profile without being logged in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Unexpected status code: {response.status_code}. Response: {response.text}"


def profile_logged(session_id: str) -> None:
    """Access the profile while logged in."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"Failed to access profile: {response.text}"
    assert "email" in response.json(), "Email not found in response."


def log_out(session_id: str) -> None:
    """Log out by deleting the session."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, f"Failed to log out: {response.text}"


def reset_password_token(email: str) -> str:
    """Request a password reset token."""
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, f"Failed to get reset token: {response.text}"
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password using a reset token."""
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200, f"Failed to update password: {response.text}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
