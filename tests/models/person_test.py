from pandora.models import Person
from tests.conftest import generate_mocked_relationship


class TestFriendsAttribute:
    def test_friends_attribute_returns_list_of_persons_instead_of_relationships(self):
        luca = Person(id=1)
        paula = Person(id=2)
        ana = Person(id=3)

        luca.personal_friends = [
            generate_mocked_relationship(luca, paula),
            generate_mocked_relationship(luca, ana)
        ]
        expected_list = [paula, ana]
        assert expected_list == luca.friends


class TestCommonFriendsMethod:

    def test_return_empty_list_if_there_is_no_common_friend_between_2_persons(self):
        luca = Person(id=1)
        paula = Person(id=2)
        fred = Person(id=3)

        luca.personal_friends = [generate_mocked_relationship(luca, fred)]
        paula.personal_friends = []

        assert [] == luca.common_friends_with(paula)

    def test_return_only_common_friends(self):
        luca = Person(id=1)
        paula = Person(id=2)
        fred = Person(id=3)
        ana = Person(id=4)
        mike = Person(id=5)

        luca.personal_friends = [
            generate_mocked_relationship(luca, fred),
            generate_mocked_relationship(luca, ana)
        ]

        paula.personal_friends = [
            generate_mocked_relationship(paula, ana),
            generate_mocked_relationship(paula, mike)
        ]

        assert [ana] == luca.common_friends_with(paula)
