# -*- encoding: utf-8 -*-


from __future__ import absolute_import
from celery import Celery, Task

class ContextTask(Task):

    # def __call__(self, *args, **kwargs):
    #     with app.app_context():
    #         return self.run(*args, **kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('on failure')
        pass


celery_app = Celery(__name__,
                    task_cls=ContextTask,
                    include=['app.async_tasks'])
# 定时任务
celery_app.conf['CELERYBEAT_SCHEDULE'] = {
        'update-access-token-every-5-minutes': {
                    'task': 'task_name',
                    'schedule': 3 * 60,
                },
}

