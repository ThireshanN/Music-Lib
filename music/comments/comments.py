
from wtforms import IntegerField, SubmitField, SelectField, StringField, HiddenField, TextAreaField


from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from music.authentication.authentication import login_required

import music.adapters.repository as repo
from music.domainmodel.track import Track
from music.comments import services

# Configure Blueprint.
import music.utilities.utilities as utilities

comments_blueprint = Blueprint(
    'comments_bp', __name__)






@comments_blueprint.route('/comment', methods=['GET', 'POST'])
@login_required
def comment_on_article():
    # Obtain the user name of the currently logged in user.
    #user_name = session['user_name']
    track_id = request.args.get('track')
    print(track_id)
    print(type(track_id))
    #print(user_name)
    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    print("test1")
    form = CommentForm()
    print("test2")

    if form.validate_on_submit():
        print("test3")
        print(form.track_id.data)
        # Use the service layer to store the new comment.
        services.add_comment(int(form.track_id.data), form.comment.data, int(form.rating.data),  repo.repo_instance)
        print("test4")
        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('comments_bp.comment_on_article', track=form.track_id.data))
        #return redirect(url_for('home_bp.home'))
    print("test2a")
    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        track_id = int(request.args.get('track'))

        # Store the article id in the form.
        form.track_id.data = track_id
        print(form.track_id.data)
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        track_id = int(form.track_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.

    reviews= services.get_reviews(repo.repo_instance)
    track = services.get_track_by_id(int(track_id), repo.repo_instance)
    k = int(track_id)
    if k not in reviews:
        curr_iter_tracks = None
        prev_tracks_url = None
        next_tracks_url = None
    else:
        comments = reviews[k]
        #comments = rev_list.reverse()
        print("test1")
        print('test1/1')
        '''
        for ele in comments:
            print(ele)
        print("test2")
        print(type(comments))
        '''
        comment = comments[0]
        print('test1/2')
        comments_per_page = 5
        cursor = request.args.get('cursor')
        print('test1/3')
        if cursor is None:
            cursor = 0
        else:
            cursor = int(cursor)
        print('test1/4')
        next_tracks_url = None
        prev_tracks_url = None

        prev_track = next_track = None
        if len(comments) > 0:
            try:
                print('test1/5')
                index = utilities.track_index_subclass(comment, comments)
                print('test1/5')
                for stored_track in reversed(comments[0:index]):
                    print('test1/5')
                    if stored_track.track_id < track.track_id:
                        print('test1/5')
                        prev_track = stored_track.track_id
                        print('test1/5')
                        break
            except ValueError:
                print("mem repo get prev track")
                pass

            try:
                index = utilities.track_index_subclass(comment, comments)
                for stored_track in comments[index + 1:len(comments)]:
                    if stored_track > track:
                        next_track = stored_track
                        break
            except ValueError:
                print("mem repo get next track")
                pass
        curr_iter_tracks = comments[cursor:cursor + comments_per_page]

        if cursor > 0:
            prev_tracks_url = url_for('comments_bp.comment_on_article', track=track_id, cursor=cursor - comments_per_page)
        if cursor + comments_per_page < len(comments):
            next_tracks_url = url_for('comments_bp.comment_on_article', track=track_id, cursor=cursor + comments_per_page)
    print('test1/6')
    return render_template(
        'tracks/track_comments.html',
        track_name=track.title,
        track_id=track_id,
        form=form,
        handler_url=url_for('comments_bp.comment_on_article'),
        tracks=curr_iter_tracks,
        prev_tracks_url = prev_tracks_url,
        next_tracks_url=next_tracks_url
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    choices = [('1', '1'),
               ('2', '2'),
               ('3', '3'),
               ('4', '4'),
               ('5', '5')]
    rating = SelectField('Rating:', choices=choices)
    comment = TextAreaField('Comment:', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    track_id = HiddenField("Track id")
    submit = SubmitField('Submit')