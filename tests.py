import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points_below_min():
    with pytest.raises(Exception):
        Question(title='q1', points=0)


def test_create_question_with_invalid_points_above_max():
    with pytest.raises(Exception):
        Question(title='q1', points=101)


def test_create_question_with_default_values():
    question = Question(title='q1')
    assert question.points == 1
    assert question.max_selections == 1
    assert question.choices == []


def test_add_choice_returns_created_choice():
    question = Question(title='q1')
    choice = question.add_choice('a')

    assert choice in question.choices
    assert choice.id == 1
    assert choice.text == 'a'
    assert choice.is_correct is False


def test_add_multiple_choices_generate_sequential_ids():
    question = Question(title='q1')

    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')

    assert [c1.id, c2.id, c3.id] == [1, 2, 3]


def test_add_choice_with_empty_text_raises_exception():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('', False)


def test_add_choice_with_text_longer_than_100_raises_exception():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('a' * 101, False)


def test_remove_choice_by_id_removes_only_target_choice():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')

    question.remove_choice_by_id(c1.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == c2.id
    assert question.choices[0].text == 'b'


def test_remove_choice_by_invalid_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices_clears_question_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert question.choices == []