import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from .models import Room
from users.models import User
from .serializers import RoomSerializer
from asgiref.sync import async_to_sync
from .xiangqi import Validator, XIANGQI_STATUS

class RoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        self.user = self.scope['user']
        print('user o day ne', self.user)
        
        if self.user.is_anonymous:
            self.close()

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # Username joined the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': self.user.username + ' has joined the room.'
            }
        )
        
        room = Room.objects.get(slug=self.room_name)
        room.push_user()
        room.save()
        room_serializer = RoomSerializer(room)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'room_state',
                'message': room_serializer.data
            }
        )

    def disconnect(self, close_code):
        print('remove user', self.user.username)
        room = Room.objects.get(slug=self.room_name)
        
        if room.is_player(self.user) and room.game_status == XIANGQI_STATUS.PLAYING:
            room.set_resign_safe_mode(self.user)

        room.remove_player_safe_mode(self.user)
        room.pop_user()
        room.save()

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        room_serializer = RoomSerializer(room)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'room_state',
                'message': room_serializer.data
            }
        )

        if room.is_empty():
            room.delete()

    # Receive message from WebSocket. Handle many types of messages
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('text_data_json:', text_data_json)

        event_type = text_data_json['type']
        message = text_data_json['message']

        if event_type == 'chat_message':
            # send message to room group, also send the type of message
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        
        elif event_type == 'xiangqi_side':
            room = Room.objects.get(slug=self.room_name)
            room.set_player_safe_mode(self.user, message['isWhite'])
            room.save()

            room_serializer = RoomSerializer(room)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'room_state',
                    'message': room_serializer.data
                }
            )

        elif event_type == 'xiangqi_ready':
            room = Room.objects.get(slug=self.room_name)
            room.set_ready_safe_mode(self.user)
            room.save()

            if room.is_ready():
                room.init_game()
                room.save()

            room_serializer = RoomSerializer(room)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'room_state',
                    'message': room_serializer.data
                }
            )

        elif event_type == 'xiangqi_resign':
            room = Room.objects.get(slug=self.room_name)
            room.set_resign_safe_mode(self.user)
            room.save()

            room_serializer = RoomSerializer(room)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'room_state',
                    'message': room_serializer.data
                }
            )

        elif event_type == 'xiangqi_move':
            room = Room.objects.get(slug=self.room_name)
            if room.game_status == XIANGQI_STATUS.PLAYING and room.is_player(self.user, room.is_white_turn):
                fen_before_move_made: str = room.fen
                fen_after_move_made: str = fen_before_move_made
                move_made: bool = False

                validator = Validator()
                loaded: bool = validator.load(fen_before_move_made)
                if loaded:
                    move_made = validator.make_move_from_uci(message['uci'])
                    if move_made:
                        if validator.is_game_over():
                            room.set_game_over(validator.get_status())

                        fen_after_move_made = validator.get_fen()
                        room.fen = fen_after_move_made
                        room.is_white_turn = validator.is_white_turn()
                        room.save()

                        room_serializer = RoomSerializer(room)

                        async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            {
                                'type': 'xiangqi_move',
                                'message': {
                                    'fen_before_move_made': fen_before_move_made,
                                    'uci': message['uci'],
                                    'room_state': room_serializer.data,
                                }
                            }
                        )

            else:
                print('not your turn')

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    def xiangqi_move(self, event):
        message = event['message']

        # Handle the board here
        print('xiangqi_move:', message)
        print('who am i:', self.user.username)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'xiangqi_move',
            'message': message
        }))



    def room_state(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'room_state',
            'message': message
        }))

class ServerConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['server_name']
        self.room_group_name = 'server_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        print('connected to server:', self.room_name)

    # when the websocket is disconnected, disconnect from the name group
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        event_type = text_data_json['type']

        if event_type == 'create_room':
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'room_list',
                    'message': message
                }
            )

    # Receive message from room group
    def room_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'room_message',
            'message': message
        }))

    def room_list(self, event):
        message = event['message']
        print('room_list:', message)
        print('server', self.room_name)

        # get all rooms
        rooms = Room.objects.filter(slug__startswith=self.room_name)
        serializer = RoomSerializer(rooms, many=True)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'room_list',
            'message': serializer.data
        }))