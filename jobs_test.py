from requests import get, post, put, delete

# Какой метод хотите протестить
__method = 'delete'


class Tester:
    def get(self):
        print(get('http://localhost:5000/api/v2/jobs').json())  # Correct
        print(get('http://localhost:5000/api/v2/jobs/1').json())  # Correct
        print(get('http://localhost:5000/api/v2/jobs/12').json())  # Incorrect

    def post(self):
        print(post('http://localhost:5000/api/v2/jobs', json={
            'leader_id': 1,
            'job': 'awd',
            'work_size': 123,
            'collaborators': '1, 2',
            'is_finished': False
        }).json())  # Correct
        print(get('http://localhost:5000/api/v2/jobs').json())

        print(post('http://localhost:5000/api/v2/jobs').json())  # Incorrect
        print(get('http://localhost:5000/api/v2/jobs').json())

        print(post('http://localhost:5000/api/v2/jobs', json={
            'job': 'LOL'
        }).json())  # Incorrect
        print(get('http://localhost:5000/api/v2/jobs').json())

    def put(self):
        print(put('http://localhost:5000/api/v2/jobs/999').json())
        print(put('http://localhost:5000/api/v2/jobs/1').json())

        # Correct
        print(put('http://localhost:5000/api/v2/jobs/1', json={
            'job': '123'
        }).json())
        print(get('http://localhost:5000/api/v2/jobs').json())

    def delete(self):
        print(delete('http://localhost:5000/api/v2/jobs/999').json())  # Incorrect

        # Correct
        print(delete('http://localhost:5000/api/v2/jobs/1').json())
        print(get('http://localhost:5000/api/v2/jobs').json())


if __name__ == '__main__':
    tester = Tester()
    method = getattr(tester, __method)
    method()
