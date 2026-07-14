import pytest
import pytest_asyncio
import bcrypt
import asyncio
from schemas.person import PersonLoginSchema, PersonSchema
from services.person_service import PersonService
from controllers.person_controller import PersonController
from database.models.person import PersonOrm

@pytest.mark.asyncio
class TestPerson:
    async def test_get_persons_empty(self, session):
        persons = await PersonService.get_all(session)
        assert persons == []

    async def test_get_persons_with_data(self, session, create_test_person):

        persons = await PersonService.get_all(session)

        assert len(persons) == 1
        assert persons[0].name == "Test User"

    async def test_get(self, session, create_test_person):
        id = 1
        person = await PersonService.get(1, session)
        assert person.id == 1
        assert person.name == "Test User"

    async def test_create(self, session):

        new_user = PersonLoginSchema(name='Test user', password='1234')

        person = await PersonService.create(new_user, session)
        assert person.name == new_user.name
        assert bcrypt.checkpw(
            new_user.password.encode('utf-8'),
            person.hashpassword.encode('utf-8')
        )

    async def test_delete(self, session):
        person = await PersonService.create(PersonLoginSchema(name='Test user', password='1234'), session)
        assert await PersonService.delete(person.id, session)

    async def test_update(self, session):
        person = await PersonService.create(PersonLoginSchema(name='Test user', password='1234'), session)

        update_data = PersonSchema(name='Niko', email='hello@mail.com', phone='+799999999999')
        updated_person = await PersonService.update(person.id, update_data, session)
        assert updated_person.id == person.id
        assert updated_person.name == person.name
        assert updated_person.email == person.email
        assert updated_person.phone == person.phone

class TestPersonController:
    async def test_get_person_empty(self):
        pass

