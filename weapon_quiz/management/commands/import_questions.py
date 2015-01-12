import re

from django.core.management.base import BaseCommand, CommandError

from multichoice.models import MCQuestion, Answer
from quiz.models import Quiz

class Command(BaseCommand):
    args = '<data_file>'
    help = 'Imports questions from text file'

    def handle(self, filename, *args, **options):
        verbosity = int(options.get('verbosity', '1'))
        
        data_file = open(filename, 'r')
        state = None
        question_count = 0
        quiz = None
        quiz_index = 0
        while not quiz:
            quiz_url = "quiz%d" % quiz_index
            if not Quiz.objects.filter(url=quiz_url):
                quiz = Quiz()
            else:
                quiz_index += 1
                continue
            quiz.title = 'Imported quiz #%d' % quiz_index
            quiz.url = quiz_url
            quiz.save()

        answers = {}
        question = None

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
                answers = {}
                question = MCQuestion()
                question.content = text
                question.save()
                quiz.question_set.add(question)
                if verbosity >= 2:
                    self.stdout.write(u'Question #%s: %s' % (num, text))
                state = 'variant'

            elif state == 'variant':
                variant = Answer()
                variant.content = text
                variant.question = question
                variant.save()
                answers[num] = variant
                if verbosity >= 2:
                    self.stdout.write(u'Variant #%s: %s' % (num, text))

            elif state == 'answer':
                answer = match.group('answer')
                variant = answers[answer]
                variant.correct = True
                variant.save()
                if verbosity >= 2:
                    self.stdout.write('Right answer: %s' % answer)
                question_count += 1
                state = None

        data_file.close()

        self.stdout.write('Imported %d questions' % question_count)
        self.stdout.write('Quiz title: %s' % quiz.title)
