# Since we are removing SQLAlchemy, we will define the models using plain Python classes and psycopg2 for database interactions.

class Epic:
    def __init__(self, id, summary, description, project_key, custom_fields):
        self.id = id
        self.summary = summary
        self.description = description
        self.project_key = project_key
        self.custom_fields = custom_fields
        self.stories = []

class Story:
    def __init__(self, id, summary, description, project_key, custom_fields, epic_id):
        self.id = id
        self.summary = summary
        self.description = description
        self.project_key = project_key
        self.custom_fields = custom_fields
        self.epic_id = epic_id
        self.tasks = []

class Task:
    def __init__(self, id, summary, description, project_key, custom_fields, story_id):
        self.id = id
        self.summary = summary
        self.description = description
        self.project_key = project_key
        self.custom_fields = custom_fields
        self.story_id = story_id
        self.test_cases = []

class TestCase:
    def __init__(self, id, summary, description, project_key, custom_fields, task_id):
        self.id = id
        self.summary = summary
        self.description = description
        self.project_key = project_key
        self.custom_fields = custom_fields
        self.task_id = task_id
