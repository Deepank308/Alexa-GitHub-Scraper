"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6
For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib, json, time, urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        # 'card': {
        #     'type' : 'Simple',
        #     'title': title,
        #     'content': output
        # },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def continue_dialog(sessionAttributes):
    
    message = {}
    message['shouldEndSession'] = False
    message['directives'] = [{'type': 'Dialog.Delegate'}]
    
    return build_response(sessionAttributes, message)

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Amazon Alexa GitHub Skills Kit. " \
                    "Please tell me your username by saying link to Username, " \
                    "and then follow the voice guide."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your username by saying link to Username, " \
                    "and then follow the voice guide."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Amazon Alexa GitHub Skills Kit. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        

def outputTryAgain(session) :
    '''
    Ask the user to try again
    '''
    sessionAttributes = session['attributes']
    card_title = "Try again"
    speech_output = "Please try again. I failed to catch you."

    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
    
def openGitHub() :
    '''
    Ask the user for the user name
    '''
    card_title = "Personalise your experience"
    speech_output = "Please enter your Username "
    
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def getUsername(intent, session) :
    '''
    Parse the user name entered by the user
    '''
    session_attributes = {}

    session_attributes['username'] = intent['slots']['username']['value']
    card_title = "Username"
    speech_output = "Thanks! We are now linked to :" + session_attributes['username'] + \
                    ". Please mention the service you want to use by saying commit/issue/pull requests/forks/stars."
    
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def getCommit(intent_request, session) :
    '''
        Ask for the repository name
    '''
    
    sessionAttributes = session['attributes']
    card_title = "Commit to Repo redirect"
    
    dialog_state = intent_request['dialogState']

    if dialog_state in ("STARTED", "IN_PROGRESS"):
        return continue_dialog(sessionAttributes)
    
    sessionAttributes['date'] = intent_request['intent']['slots']['date']['value']
    speech_output = "For which repo you want to see the commit"
      
    sessionAttributes['work'] = "commits"
    
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def getIssue(intent_request, session) :
    '''
        Ask for the repository name
    '''
    
    sessionAttributes = session['attributes']
    card_title = "Issue to Repo redirect"
      
    dialog_state = intent_request['dialogState']

    if dialog_state in ("STARTED", "IN_PROGRESS"):
        return continue_dialog(sessionAttributes)
    
    sessionAttributes['repo'] = intent_request['intent']['slots']['repo']['value']
    
    html = urlopen("https://github.com/" + sessionAttributes['username'] + "/" + sessionAttributes['repo'])
    soup = BeautifulSoup(html.read())
    
    page_nav = soup.find("nav", {"class" : "reponav js-repo-nav js-sidenav-container-pjax container"})
    spans = page_nav.find_all("span", {"class" : "Counter"})
    
    num_issues = spans[0].get_text()
    
    speech_output = "There are " + str(num_issues) + " issue(s) for " + sessionAttributes['repo']
    
    sessionAttributes['work'] = "issues"
    
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def getPullRequest(intent_request, session) :
    '''
        Ask for the repository name
    '''
    
    sessionAttributes = session['attributes']
    card_title = "Pull request to Repo redirect"
      
    dialog_state = intent_request['dialogState']

    if dialog_state in ("STARTED", "IN_PROGRESS"):
        return continue_dialog(sessionAttributes)
    
    sessionAttributes['repo'] = intent_request['intent']['slots']['repo']['value']
    
    html = urlopen("https://github.com/" + sessionAttributes['username'] + "/" + sessionAttributes['repo'])
    soup = BeautifulSoup(html.read())
    
    page_nav = soup.find("nav", {"class" : "reponav js-repo-nav js-sidenav-container-pjax container"})
    spans = page_nav.find_all("span", {"class" : "Counter"})
    
    num_pull_request = spans[1].get_text()
    
    speech_output = "There are " + str(num_pull_request) + " pull request(s) for " + sessionAttributes['repo']
    
    sessionAttributes['work'] = "Pull request"
    
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def getRepository(intent, session) : 
    ''' 
        Check for the commit on the specified date
    '''
    
    sessionAttributes = session['attributes']
    card_title = "Repo scraper"
    # speech_output = "This part is currently under construction... Sorry for Inconvenience"
    repo_name = intent['slots']['repository']['value']
    
    git_repo_link = "https://www.github.com/" + sessionAttributes['username'] + "/" + repo_name + "/" + sessionAttributes['work'] + "/master"
    
    speech_output = "Please go through this link to see the " + sessionAttributes['work'] + " : " + git_repo_link
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def getForks(intent_request, session) :
    '''
    This function returns the number of forks for the user asked repo
    '''
    sessionAttributes = session['attributes']
    card_title = "Forks"
    
    dialog_state = intent_request['dialogState']

    if dialog_state in ("STARTED", "IN_PROGRESS"):
        return continue_dialog(sessionAttributes)
    
    repo_name = intent_request['intent']['slots']['repo']['value']
    
    html = urlopen("https://github.com/" + sessionAttributes['username'] + "/" + repo_name)
    soup = BeautifulSoup(html.read())
    
    page_head = soup.find("ul", {"class" : "pagehead-actions"})
    
    i = 2 ## for forks
    page_head_li = page_head.find_all("li")
    page_head_li[i] = page_head_li[i].get_text()
    page_head_li[i] = str(page_head_li[i])
    page_head_li[i] = page_head_li[i].replace(" ", "")
    page_head_li[i] = page_head_li[i].replace("\n", "")

    num_forks = page_head_li[i][4 :]
    
    speech_output = "There are " + str(num_forks) + " fork(s) for " + str(repo_name)
    # print(soup)
    
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
    

def getStars(intent_request, session) :
    '''
    This function returns the number of forks for the user asked repo
    '''
    sessionAttributes = session['attributes']
    card_title = "Stars"
    
    dialog_state = intent_request['dialogState']

    if dialog_state in ("STARTED", "IN_PROGRESS"):
        return continue_dialog(sessionAttributes)
    
    repo_name = intent_request['intent']['slots']['repo']['value']
    
    html = urlopen("https://github.com/" + sessionAttributes['username'] + "/" + repo_name)
    soup = BeautifulSoup(html.read())
    
     
    page_head = soup.find("ul", {"class" : "pagehead-actions"})
    
    i = 1 ## for stars
    page_head_li = page_head.find_all("li")
    page_head_li[i] = page_head_li[i].get_text()
    page_head_li[i] = str(page_head_li[i])
    page_head_li[i] = page_head_li[i].replace(" ", "")
    page_head_li[i] = page_head_li[i].replace("\n", "")

    
    num_stars = page_head_li[i][4 :]
    
    speech_output = "There are " + str(num_stars) + " star(s) for " + str(repo_name)
    # print(soup)
    
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
          
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    try :
        # Dispatch to your skill's intent handlers
        if intent_name == "opengithub":
            return openGitHub()
        if intent_name == "usernameInput":
            return getUsername(intent, session)
        elif intent_name == "commit":
            return getCommit(intent_request, session)
        elif intent_name == "issue" :
            return getIssue(intent_request, session)
        elif intent_name == "pullrequest" :
            return getPullRequest(intent_request, session)
        elif intent_name == "repositoryName":
            return getRepository(intent, session)
        elif intent_name == "forks" :
            return getForks(intent_request, session)
        elif intent_name == "stars" :
            return getStars(intent_request, session)
        elif intent_name == "AMAZON.HelpIntent":
            return get_welcome_response()
        elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
            return handle_session_end_request()
        else:
            raise ValueError("Invalid intent")
    except :
        return outputTryAgain(session)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
        
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
        
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
