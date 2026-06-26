import pytest
from sqlalchemy.exc import ProgrammingError
from core.security import is_admin_user, store_refresh_token
from models import User, Role, UserRole


@pytest.mark.asyncio
async def test_is_admin_user_accepts_role_assignment(monkeypatch):
    class DummyResult:
        def __init__(self, rows):
            self.rows = rows

        def all(self):
            return self.rows

        def scalars(self):
            return DummyResult([row[0] if isinstance(row, tuple) else row for row in self.rows])

        def first(self):
            return self.rows[0] if self.rows else None

    class DummySession:
        def __init__(self, rows):
            self.rows = rows

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def execute(self, query):
            return DummyResult(self.rows)

    class DummyUser:
        user_id = 1

    monkeypatch.setattr("core.security.get_session", lambda: DummySession([("admin",)]))

    assert await is_admin_user(DummyUser()) is True


@pytest.mark.asyncio
async def test_store_refresh_token_handles_missing_table(monkeypatch):
    class DummySession:
        def __init__(self):
            self.added = []

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        def add(self, value):
            self.added.append(value)

        async def rollback(self):
            return None

        async def commit(self):
            raise ProgrammingError("INSERT", None, Exception("relation \"refresh_tokens\" does not exist"))

    monkeypatch.setattr("core.security.get_session", lambda: DummySession())

    await store_refresh_token(1, "refresh-token")
