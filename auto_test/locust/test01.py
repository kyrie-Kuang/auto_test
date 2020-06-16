from locust import TaskSet, task, HttpLocust


class UserBehavior(TaskSet):

    @task
    def Baidu_index(self):
        self.client.get("/")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000