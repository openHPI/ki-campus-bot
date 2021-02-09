from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted
from sanic.request import Request
from rasa_sdk.executor import CollectingDispatcher

import requests
import json

class CourseSet(Action):
	def name(self):
		return "action_course_set"

	def run(self, dispatcher, tracker, domain):
		currentCourse = tracker.get_slot('current_course')
		if currentCourse:
			return [SlotSet('course-set', True)]
		else:
			return [SlotSet('course-set', False)]

class SetCurrentCourse(Action):
	def name(self):
		return "action_set_current_course"

	def run(self, dispatcher, tracker, domain):
		currentCourse = tracker.latest_message['text']
		return [SlotSet('current_course', currentCourse)]

class ActionGetCourses(Action):
	def name(self) -> Text:
		return "action_get_courses"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		current_state = tracker.current_state()
		token = current_state['sender_id']
		r = requests.get('http://localhost:3000/bridges/chatbot/my_courses', headers={"content-type": "application/json",
		"Authorization": 'Bearer {0}'.format(token)})
		status = r.status_code
		if status == 200:
			response = json.loads(r.content)
			dispatcher.utter_message('You are currently enrolled in these courses:')
			for course in response:
				title = course['title']
				dispatcher.utter_message(title)
			return [SlotSet('all_courses', response)]
		else:
			return []

	class ActionGetAchievements(Action):
		def name(self) -> Text:
			return "action_get_achievements"

		def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
			current_state = tracker.current_state()
			token = current_state['sender_id']
			currentCourse = tracker.slots['current_course']
			courseId = 0
			allCourses = tracker.slots['all_courses']
			for course in allCourses:
				if course['title'] == currentCourse:
					courseId = course['id']
			r = requests.get('http://localhost:3000/bridges/chatbot/my_courses/{0}/achievements'.format(courseId), headers={"content-type": "application/json",
			"Authorization": 'Bearer {0}'.format(token)})
			status = r.status_code
			if status == 200:
				response = json.loads(r.content)
				for achievement in response:
					dispatcher.utter_message('{0}: {1}'.format(achievement['name'], achievement['description']))
					if achievement['achieved']:
						return[SlotSet('current_course_achieved', True)]
					else:
						return[SlotSet('current_course_achieved', False)]
			else:
				return []

	class ActionGetCertificate(Action):
		def name(self) -> Text:
			return "action_download_certificate"

		def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
			dispatcher.utter_message('Here is your certificate!')
			return []
