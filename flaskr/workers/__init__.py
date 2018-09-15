from celery import Celery

class CeleryX(Celery):
    def __init__(self, app):
        super().__init__(
            backend=app.config['CELERY_RESULT_BACKEND'],
            broker=app.config['CELERY_BROKER_URL']
        )
        class ContextTask(self.Task):
            abstract = True
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        self.Task = ContextTask
