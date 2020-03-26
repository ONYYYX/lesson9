from requests import get, post, put, delete

# Какой метод хотите протестить
__method = 'delete'


class Tester:
    def get(self):
        print(get('http://localhost:5000/api/v2/users').json())  # Correct
        print(get('http://localhost:5000/api/v2/users/1').json())  # Correct
        print(get('http://localhost:5000/api/v2/users/12').json())  # Incorrect
        print(get('http://localhost:5000/api/v2/users/awd').json())  # Incorrect

    def post(self):
        print(post('http://localhost:5000/api/v2/users', json={
            'name': 'alwdll',
            'surname': 'LOL',
            'age': 123,
            'position': '123123',
            'speciality': 'adwawd',
            'address': 'awdawd',
            'email': 'oawd@awd.ru',
            'city_from': 'Moscow'
        }).json())  # Correct
        print(get('http://localhost:5000/api/v2/users').json())

        print(post('http://localhost:5000/api/v2/users').json())  # Incorrect
        print(get('http://localhost:5000/api/v2/users').json())

        print(post('http://localhost:5000/api/v2/users', json={
            'job': 'LOL'
        }).json())  # Incorrect
        print(get('http://localhost:5000/api/v2/users').json())

    def delete(self):
        print(delete('http://localhost:5000/api/v2/users/awdd').json())  # Incorrect
        print(delete('http://localhost:5000/api/v2/users/999').json())  # Incorrect

        # Correct
        print(delete('http://localhost:5000/api/v2/users/1').json())
        print(get('http://localhost:5000/api/v2/users').json())


if __name__ == '__main__':
    tester = Tester()
    method = getattr(tester, __method)
    method()
