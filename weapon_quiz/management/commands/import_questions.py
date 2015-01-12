import re
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<quiz_id> <data_file>'
    help = 'Imports questions from text file'

    def handle(self, quiz_id, filename, *args, **options):
        data_file = open(filename, 'r')
        state = None
        question_count = 0
        for line in data_file:
            match = re.match(r'^ *(?P<answer>\d+) *\.? *$', line)
            if match:
                state = 'answer'
            else:
                match = re.match(r'^ *(?P<num>\d+) *\. *(?P<text>.+)$', line)
                num, text = match.groups()
                text = text.decode('utf-8')

            if not state:
                #question start
                self.stdout.write(u'Question #%s: %s' % (num, text))
                state = 'variant'

            elif state == 'variant':
                self.stdout.write(u'Variant #%s: %s' % (num, text))

            elif state == 'answer':
                self.stdout.write('Right answer: %s' % match.group('answer'))
                question_count += 1
                state = None

            if question_count >= 3:
                break
        data_file.close()

        self.stdout.write('Imported %d questions' % question_count)
