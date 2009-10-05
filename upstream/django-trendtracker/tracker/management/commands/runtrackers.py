from django.core.management.base import CommandError
from django.core.management.base import NoArgsCommand
from tracker.models import Tracker, Channel
from livesearch.models import *
from yql.search import *

class Command(NoArgsCommand):
    help = 'Runs trackers.'
    channels = dict()
    
    def handle_noargs(self, **options):
        self.inject()
        self.fetch()
        self.parse()
        self.index()

    def inject(self):
        pending_trackers = Tracker.objects.filter(status=Tracker.PENDING)
        for tracker in pending_trackers:
            for channel in tracker.packs.all():
                if channel.id in self.channels:
                    self.channels[channel.id].update({tracker.query: 0})
                else:
                    self.channels[channel.id] = dict()

        for id, queries in self.channels.items():
            self.channels[id] = queries.keys()

    def fetch(self):
        for channel_id, queries in self.channels.items():
            channel = Channel.objects.get(id=channel_id)
            api_class = globals()[channel.api]
            api = api_class()
            if issubclass(api_class, PipeSearch):
                api.init_options()
            for query in queries:
                result = api.fetch(query)
                print result

    def parse(self):
        pass

    def index(self):
        pass