from django.test import TestCase
from django.urls import reverse
from login.models import CustomUser
from login.managers import CustomUserManager
from .models import TaskList, Feedback
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class ViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(email='testingAuto@gmail.com',first_name = 'tester', last_name = 'testing', password='password@1234')

        # Create test tasks
        self.task1 = TaskList.objects.create(task='Task 1', category = 'test1', manage=self.user)
        self.task2 = TaskList.objects.create(task='Task 2', category = 'test2', manage=self.user, done=True)
        self.task3 = TaskList.objects.create(task='Task 3', category = 'test3',  manage=self.user)

        # Create test feedback
        self.feedback_data = {'feedback_text': 'Test feedback'}

    def test_index_view_with_alert(self):
        self.client.login(email='testingAuto@gmail.com', password='password@1234')
        # Set a task deadline less than a day from now
        self.task1.deadline = timezone.now() + timezone.timedelta(hours=23)
        self.task1.save()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['alert_message'])

    def test_todo_list_view_with_filters(self):
        self.client.login(email='testingAuto@gmail.com', password='password@1234')
        # Test filtering by completed tasks
        response = self.client.get(reverse('todolist') + '?filter=completed')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['all_tasks'], [repr(self.task2)])
        # Test filtering by incomplete tasks
        response = self.client.get(reverse('todolist') + '?filter=incomplete')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['all_tasks'], [repr(self.task1), repr(self.task3)])

    def test_add_task_view(self):
        self.client.login(email='testingAuto@gmail.com', password='password@1234')
        task_data = {'task': 'New Task', 'category': 'New Category'}
        response = self.client.post(reverse('add_task'), task_data)
        self.assertEqual(response.status_code, 302)  # Check if redirection happens after task addition
        # Check if the task is actually added
        self.assertTrue(TaskList.objects.filter(task='New Task', category='New Category').exists())

   

    def test_completed_view_pagination(self):
        self.client.login(email='testingAuto@gmail.com', password='password@1234')
        # Create more completed tasks for pagination test
        for i in range(10):
            TaskList.objects.create(task=f'Task {i}', manage=self.user, done=True)
        response = self.client.get(reverse('completed'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['all_tasks']), 3)  # Test pagination limit

    def test_profile_view(self):
        self.client.login(email='testingAuto@gmail.com', password='password@1234')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['email'], 'testingAuto@gmail.com')  # Assuming email is set to example value
        self.assertEqual(response.context['total_points'], 0)  # Assuming initial points are 0


