# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from gcloud.taskflow3.models import TaskFlowInstance
from gcloud.taskflow3.signals import taskflow_started, taskflow_finished, taskflow_revoked
from gcloud.contrib.function.models import FunctionTask


@receiver(post_save, sender=TaskFlowInstance)
def function_task_create_handler(instance, created, **kwargs):
    if created and instance.flow_type == "common_func":
        FunctionTask.objects.create(
            task=instance, creator=instance.creator,
        )


@receiver(taskflow_started)
def function_task_started_handler(task_id, **kwargs):
    FunctionTask.objects.filter(task_id=task_id).update(status="executed")


@receiver(taskflow_finished)
def function_task_finished_handler(task_id, **kwargs):
    FunctionTask.objects.filter(task_id=task_id).update(status="finished")


@receiver(taskflow_revoked)
def function_task_revoked_handler(task_id, **kwargs):
    FunctionTask.objects.filter(task_id=task_id).update(status="finished")
