from django.core.management.base import BaseCommand
from django.contrib.auth import hashers
from SO.models import Tag, Answer, Question, ReactionToQuestion, Profile, User
from random import  choice
from django.db import IntegrityError

class Command(BaseCommand):
    help = '''
            - ratio tags
            - ratio users
            - ratio*10 questions
            - ratio*100 answers
            - ratio*200 reactions'''

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int, help='Ratio value')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio'][0]

        TAGS_RATIO = ratio
        USERS_RATIO = ratio
        QUESTIONS_RATIO = 10*ratio
        ANSWERS_RATIO = 100*ratio
        REACTIONS_RATIO = 200*ratio


        first_tag_id = Tag.manager.last().tag_id + 1
        first_user_id = User.objects.last().id + 1
        first_profile_id = Profile.manager.last().profile_id + 1
        first_question_id = Question.manager.last().question_id + 1
        first_answer_id = Answer.manager.last().answer_id + 1
        first_reaction_id = ReactionToQuestion.objects.last().id + 1

        print("First IDs of new instances:\n"
                f"Tag: {first_tag_id}\n"
                f"User: {first_user_id}\n"
                f"Profile: {first_profile_id}\n"
                f"Question: {first_question_id}\n"
                f"Answer: {first_answer_id}\n"
                f"ReactionToQuestion: {first_reaction_id}")

        '''заполнене ratio = 10000 '''

        #  Теги
        tags = [Tag(name=f'Tag {tag_id}')
                    for tag_id in range(first_tag_id, first_tag_id + TAGS_RATIO)]
        Tag.manager.bulk_create(tags)

        self.stdout.write('Filling Tags completed with success!')

        # Пользователь
        users = [User(username=f'User{user_id}',
                        first_name=f'fName{user_id}',
                        last_name=f'lName{user_id}',
                        email=f'user{user_id}@gmail.com',
                        password=hashers.make_password(f'pass{user_id}'))
                        for user_id in range(first_user_id, first_user_id + USERS_RATIO)]
        User.objects.bulk_create(users)

        self.stdout.write('Filling Users completed with success!')

        # Профиль
        profiles = [Profile(user_id=user_id,
                            avatar='static/img/default.jpg')
                            for user_id in range(first_user_id, first_user_id + USERS_RATIO)]
        Profile.manager.bulk_create(profiles)

        self.stdout.write('Filling Profiles completed with success!')

        # Вопросы
        questions = [Question(que_user_id=first_profile_id + question_id%USERS_RATIO,
                                title=f'Question #{question_id}',
                                text=f'Text for question #{question_id}')
                                for question_id in range(first_question_id, first_question_id + QUESTIONS_RATIO)]
        Question.manager.bulk_create(questions)
        for i in range(len(questions)):
            tag_index = i % len(tags)  # Вычисляем индекс тега с помощью операции модуля
            questions[i].tags.add(tags[tag_index])


                

        self.stdout.write('Filling Questions completed with success!')

        # Ответы
        answers = [Answer(author_id=first_profile_id + answer_id%USERS_RATIO,
                            ans_question_id=first_question_id + answer_id%QUESTIONS_RATIO,
                            ans_title=f'Answer #{answer_id}',
                            ans_text=f'Answer #{answer_id}')
                            for answer_id in range(first_answer_id, first_answer_id + ANSWERS_RATIO)]
        Answer.manager.bulk_create(answers)

        self.stdout.write('Filling Answers completed with success!')

        # Лайки
        reactions = []
        for reaction_id in range(first_reaction_id, first_reaction_id + REACTIONS_RATIO):
            reaction, created = ReactionToQuestion.objects.get_or_create(
            user_like_id=first_profile_id + reaction_id % USERS_RATIO,
            question_like_id=first_question_id + reaction_id % QUESTIONS_RATIO,
            answer_like_id=first_answer_id + reaction_id % ANSWERS_RATIO,
            like=choice(("Like", "Dislike"))
        )
            if created:
                    reactions.append(reaction)  
        ReactionToQuestion.objects.bulk_create(reactions)
        self.stdout.write('Filling Evals completed with success!')