import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from buggernaut.models import Issue, Comment, Project
from buggernaut.serializers import CommentGetSerializer


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
            comment = Comment.objects.get(pk=comment_id)
            issue = comment.issue
            try:
                project = Project.objects.get(pk=issue.project.id)
                if (project.id == int(self.project_id)):
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

    # Receive message from room group
    def send_comment(self, event):
        comment = event['comment']

        # Send message to WebSocket
        self.send(text_data=json.dumps(comment))
