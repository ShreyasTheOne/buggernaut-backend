import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.auth import get_user
from .models import Issue, Comment, Project
from .serializers import CommentGetSerializer


class CommentConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_id = self.scope['url_route']['kwargs']['project_id']

    def connect(self):
        print("connecting")

        try:
            project = Project.objects.get(pk=self.project_id)
            print("no issues")
            async_to_sync(self.channel_layer.group_add)(
                self.project_id,
                self.channel_name
            )
            print(self.project_id)
            print("connected")
            self.accept()
        except Issue.DoesNotExist:
            self.close()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.project_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("received")
        comment_data_json = json.loads(text_data)
        comment_id = comment_data_json['comment_id']

        try:
            # print("comment_id")
            # print(comment_id)
            comment = Comment.objects.get(pk=comment_id)
            issue = comment.issue
            try:
                project = Project.objects.get(pk=issue.project.id)
                # print("project.id:" , type(project.id), sep=" ")
                # print("self.project_id:" , type(self.project_id), sep=" ")
                if(project.id == int(self.project_id)):
                    print("issue.id")
                    print(issue.id)
                    serializer = CommentGetSerializer(comment)
                    async_to_sync(self.channel_layer.group_send)(
                        self.project_id,
                        {
                            'type': "send_comment",
                            'comment': serializer.data,
                        }
                    )
            except Project.DoesNotExist:
                print("project not found")
                pass

        except Comment.DoesNotExist:
            pass

        # try:
        #     issue = Issue.objects.get(pk=issue_id)
        #     if issue.project == self.project_id:
        #
        #     else:
        #         pass
        # except Issue.DoesNotExist:
        #     pass


    # Receive message from room group
    def send_comment(self, event):
        comment = event['comment']

        # Send message to WebSocket
        self.send(text_data=json.dumps(comment))
