import pytest
from app.users.dao import UsersDAO


@pytest.mark.parametrize("user_id, user_email, is_exists", [  #FIXME FIX AC SCOPE
    (1, 'test@example.com', True),
    (5, 'abc', False)
])
async def test_find_user_by_id(user_id, user_email, is_exists):
    user = await UsersDAO.find_by_id(user_id)

    if is_exists:
        assert user
        assert user.email == user_email
        assert user.id == user_id
    else:
        assert not user
