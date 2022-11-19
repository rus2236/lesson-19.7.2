from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
       Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
       запрашиваем список всех питомцев и проверяем что список не пустой.
       Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Baron', animal_type='shepard', age='4', pet_photo='images/dog1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/catvader.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age='5'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


########################################################################################################

# №1
def test_add_new_pet_without_photo_valid_data(name='Барсик', animal_type='кошак', age='10'):
    """Тест на добавление питомца без фото с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# №2
def test_add_photo_of_pet(pet_photo='images/catvader.jpg'):
    '''Тест на добавление фото к питомцу'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("There is no my pets")

# №3
def test_add_pet_without_photo_with_empty_value_in_variable_name(name='', animal_type='cat', age='12'):
    '''Негативный тест. Добавление питомца с пустым значением в переменной name
    Тест не будет пройден, если питомец будет добавлен на сайт с пустым значением в поле "имя"'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] != '', 'Питомец добавлен на сайт с пустым значением в имени'

# №4
def test_add_pet_without_photo_with_empty_value_in_variable_animal_type(name='Tom', animal_type='', age='9'):
    '''Негативный тест. Добавление питомца с пустым значением в переменной animal_type
    Тест не будет пройден, если питомец будет добавлен на сайт с пустым значением в поле "порода"'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['animal_type'] != '', 'Питомец добавлен на сайт с пустым значением породы'

# №5
def test_add_pet_without_photo_with_empty_value_in_variable_age(name='Bill', animal_type='cat', age=''):
    '''Негативный тест. Добавление питомца с пустым значением в переменной age
    Тест не будет пройден, если питомец будет добавлен на сайт с пустым значением в поле "возраст"'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] != '', 'Питомец добавлен на сайт с пустым значением возраста'

# №6
def test_add_pet_without_photo_with_empty_value(name='', animal_type='', age=''):
    '''Негативный тест. Добавление питомца с пустыми значениями
    Тест не будет пройден, если питомец будет добавлен на сайт с пустыми значениями'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] != ''
    assert result['animal_type'] != ''
    assert result['age'] != '', 'Питомец добавлен на сайт с пустыми значениями'

# №7
def test_add_pet_negative_age_number(name='Bob', animal_type='dog', age='-5', pet_photo='images/dog1.jpg'):
    '''Негативный тест. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert age not in result['age'], 'Питомец добавлен на сайт с отрицательным числом в поле возраст'

# №8
def test_add_pet_with_four_digit_age_number(name='Beer', animal_type='dog', age='1234', pet_photo='images/dog1.jpg'):
    '''Негативный тест. Добавление питомца с числом более трех знаков в переменной age.
    Тест не будет пройден ели питомец будет добавлен на сайт с числом превышающим три знака в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert len(result['age']) < 4, 'Питомец добавлен на сайт с числом превышающим 3 знака в поле возраст'

# №9
def test_add_pet_with_numbers_in_variable_name(name='12345', animal_type='dog', age='5', pet_photo='images/dog1.jpg'):
    '''Негативный тест. Добавление питомца с цифрами вместо букв в переменной name.
    Тест не будет пройден если питомец будет добавлен на сайт с цифрами вместо букв в поле имя.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert name not in result['name'], 'Питомец добавлен на сайт с цифрами вместо букв в поле имя'

# №10
def test_add_pet_with_numbers_in_variable_animal_type(name='Tom', animal_type='123456', age='5', pet_photo='images/dog1.jpg'):
    '''Негативный тест. Добавление питомца с цифрами вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен на сайт с цифрами вместо букв в поле порода.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец добавлен на сайт с цифрами вместо букв в поле порода'

# №11
def test_add_pet_with_words_in_variable_age(name='Tom', animal_type='cat', age='abc', pet_photo='images/dog1.jpg'):
    '''Негативный тест. Добавление питомца с буквами вместо цифр в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с буквами вместо цифр в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert age not in result['age'], 'Питомец добавлен на сайт с цифрами вместо букв в поле возраст'

# №12
def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Негативный тест. Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# №13
def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Негативный тест. Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# №14
def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Tom', age='2', pet_photo='images/dog1.jpg'):
    '''Негативный тест. Добавления питомца название породы которого превышает 10 слов
    Тест не будет пройден если питомец будет добавлен на сайт с названием породы состоящим из более 10 слов'''

    animal_type = 'овчарка мопс кот бородач алабай дог мастиф пес кот ворона дуб береза'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count < 10, 'Питомец добавлен с названием породы больше 10 слов'

