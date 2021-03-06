"""
RAMP database helper queries
"""
from __future__ import print_function, absolute_import

from .model import Submission, Event, EventTeam


def select_submissions_by_id(session, submission_id):
    """
    Query for all submissions of given event with given status

    Parameters
    ----------
    session : `sqlalchemy.orm.Session`
        database connexion session
    event_name : str
        name of the RAMP event
    state : str
        state of the requested submissions

    Returns
    -------
    submission : `rampbkd.model.Submission`
        queried submission

    """
    submission = (session
                  .query(Submission)
                  .filter(Submission.id == submission_id)
                  .first())

    return submission


def select_submissions_by_state(session, event_name, state):
    """
    Query for all submissions of given event with given status

    Parameters
    ----------
    session :
        database connexion session
    event_name : str
        name of the RAMP event
    state : str
        state of the requested submissions

    Returns
    -------
    List of submissions : List[`rampbkd.model.Submission`]
        queried submissions

    """
    submissions = (session
                   .query(Submission)
                   .filter(Event.name == event_name)
                   .filter(Event.id == EventTeam.event_id)
                   .filter(EventTeam.id == Submission.event_team_id)
                   .filter(Submission.state == state)
                   .order_by(Submission.submission_timestamp)
                   .all())

    return submissions
