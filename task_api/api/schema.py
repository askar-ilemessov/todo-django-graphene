import graphene

from graphene_django import DjangoObjectType, DjangoListField
from .models import Task


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"


class Query(graphene.ObjectType):
    task = graphene.Field(TaskType, taks_id=graphene.ID())
    all_tasks = graphene.List(TaskType)

    def resolve_all_tasks(self, info, **kwargs):
        task_instance = Task.objects.all()
        return task_instance

    def resovle_task(self, info, task_id):
        task_instance = Task.objects.get(id=task_id)
        return task_instance


class TaskInput(graphene.InputObjectType):
    id = graphene.ID()
    task_title = graphene.String()
    task_text = graphene.String()
    task_status = graphene.String()


class CreateTask(graphene.Mutation):
    class Arguments:
        task_data = TaskInput(required=True)

    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, task_data=None):
        task_instance = Task(
            task_title=task_data.task_title,
            task_text=task_data.task_text,
            task_status=task_data.task_status
        )
        task_instance.save()
        return CreateTask(task=task_instance)


class UpdateTask(graphene.Mutation):
    class Arguments:
        task_data = TaskInput(required=True)

    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, task_data=None):
        task_instance = Task.objects.get(id=task_data.id)

        if task_instance:
            task_instance.task_title = task_data.task_title
            task_instance.task_text = task_data.task_text
            task_instance.task_status = task_data.task_status
            task_instance.save()

            return UpdateTask(task=task_instance)
        return UpdateTask(book=None)


class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, id):
        task_instance = Task.objects.get(id=id)
        task_instance.delete()
        return None


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
