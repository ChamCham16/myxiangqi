import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from .models import XiangqiRoom
from users.models import User
from .serializers import XiangqiRoomSerializer
from asgiref.sync import async_to_sync
from .xiangqi import XiangqiBoard
# from .utils.xiangqi.xiangqi import XiangqiBoard as XBoard

class XiangqiRoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        self.user = self.scope['user']
        print('user o day ne', self.user)
        
        if self.user.is_anonymous:
            self.close()

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'xiangqi_%s' % self.room_name

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
        

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        room = XiangqiRoom.objects.get(slug=self.room_name)
        if room.white == str(self.user.id):
            room.white = ''
            room.white_name = ''
            room.white_ready = False
            room.black_ready = False
            room.board = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'
            room.save()

        if room.black == str(self.user.id):
            room.black = ''
            room.black_name = ''
            room.black_ready = False
            room.white_ready = False
            room.board = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'
            room.save()


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
        
        elif event_type == 'xiangqi_color':
            room = XiangqiRoom.objects.get(slug=self.room_name)

            if message == 'white':
                if room.white == '':
                    room.white = str(self.user.id)
                    room.white_name = self.user.username
                    room.save()

                    if room.black == str(self.user.id):
                        room.black = ''
                        room.black_name = ''
                        room.save()

                elif room.white == str(self.user.id):
                    room.white = ''
                    room.white_name = ''
                    room.save()

            elif message == 'black':
                if room.black == '':
                    room.black = str(self.user.id)
                    room.black_name = self.user.username
                    room.save()

                    if room.white == str(self.user.id):
                        room.white = ''
                        room.white_name = ''
                        room.save()

                elif room.black == str(self.user.id):
                    room.black = ''
                    room.black_name = ''
                    room.save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'xiangqi_color',
                    'message': {
                        'white': room.white,
                        'black': room.black,
                        'white_name': room.white_name,
                        'black_name': room.black_name
                    }
                }
            )

        elif event_type == 'xiangqi_start':
            room = XiangqiRoom.objects.get(slug=self.room_name)

            if room.white == str(self.user.id):
                room.white_ready = not room.white_ready
                room.save()

            elif room.black == str(self.user.id):
                room.black_ready = not room.black_ready
                room.save()

            print('white_ready:', room.white_ready)
            print('black_ready:', room.black_ready)
            
            # check if both players are ready, then start the game
            if room.white_ready and room.black_ready:
                room.turn = 'white'
                room.board = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'
                room.save()

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'xiangqi_start',
                        'message': {
                            'fen': room.board,
                            'turn': room.turn,
                            'isCheck': False,
                            'isCheckmate': False,
                        }
                    }
                )

        elif event_type == 'xiangqi_move':
            room = XiangqiRoom.objects.get(slug=self.room_name)
            print('room.board before moving:', room.board)

            xBoard = XiangqiBoard(room.board)
            isValidMove = xBoard.isValidMove(message)
            print('isValidMove:', isValidMove)

            after_make_move = xBoard.makeMove(message)
            print('statusMakeMove:', after_make_move)

            if after_make_move.get('status'):
                if room.turn == 'white' and room.white == str(self.user.id):
                    room.board = room.board + ' ' + message
                    room.turn = 'black'
                    room.save()

                elif room.turn == 'black' and room.black == str(self.user.id):
                    room.board = room.board + ' ' + message
                    room.turn = 'white'
                    room.save()

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'xiangqi_move',
                        'message': {
                            'fen': room.board,
                            'turn': room.turn,
                            'isCheck': after_make_move.get('isCheck'),
                            'isCheckmate': after_make_move.get('isCheckmate'),
                        }
                    }
                )

                # if checkmate, then reset the ready status
                if after_make_move.get('isCheckmate'):
                    room.white_ready = False
                    room.black_ready = False
                    room.save()


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    def xiangqi_color(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'xiangqi_color',
            'message': message
        }))

    def xiangqi_start(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'xiangqi_start',
            'message': message
        }))

    def xiangqi_move(self, event):
        message = event['message']

        # Handle the board here

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'xiangqi_move',
            'message': message
        }))

class RoomsConsumer(WebsocketConsumer):
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

        # get all rooms
        rooms = XiangqiRoom.objects.all()
        serializer = XiangqiRoomSerializer(rooms, many=True)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'room_list',
            'message': serializer.data
        }))