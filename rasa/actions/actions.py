import pandas as pd
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType, Restarted
from rasa_sdk.types import DomainDict

class ActionGetLearningRecommendation(Action):

    def name(self) -> Text:
        return "action_get_learning_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        language = str(tracker.get_slot("language")) # englisch deutsch egal
        topic = str(tracker.get_slot("topic"))# KI-Einführung KI-Vertiefung KI-Berufsfelder KI-Gesellschaft Data Science Maschinelles Lernen egal
        level = str(tracker.get_slot("level"))# Einsteiger Fortgeschritten Experte
        startdate = bool(tracker.get_slot("startdate")) # affirm deny
        live = bool(tracker.get_slot("live")) # affirm deny
        max_duration = int(tracker.get_slot("max_duration")) # Zehn Fünfzig über Fünfzig egal
        
        ###
        # Tabelle mit Lernangeboten einlesen
        los = pd.read_excel(io="lernangebote_fuer_Chatbotstudie.xlsx", engine='openpyxl', converters={'name':str,'language':str, 'level':int, 'topics':str, 'source':str, 'exists':bool, 'duration':int, 'URL': str, 'live':bool})
        
        # language: Angebote in nicht erwünschten Sprachen löschen
        if   language.lower() == "egal": pass
        elif language.lower() == "englisch": los = los[los.language == "en"]
        elif language.lower() == "deutsch": los = los[los.language == "de"]
        else: return dispatcher.utter_message("language")
        
        # duration: Angebote mit falscher Dauer löschen 
        if   max_duration == 0:  pass  #bedeutet die Dauer ist egal
        elif max_duration <= 10: los = los[los.duration <= 10]
        elif max_duration <= 50: los = los[los.duration <= 50]
        elif max_duration >  50: los = los[los.duration >  50]
        else: return dispatcher.utter_message("max_duration")       

        # level: Angebote mit falschem Niveau löschen
        if   level.lower() == "einsteiger": los = los[los.level == 1]
        elif level.lower() == "fortgeschritten": los = los[los.level == 2]
        elif level.lower() == "experte": los = los[los.level == 3]
        else: return dispatcher.utter_message("level")

        # exists: Angebote löschen, die noch nicht existieren (falls gewünscht)
        if startdate == "True":
            los = los[los.exists == 1]
        

        # live: Angebote löschen, die auch live stattfinden (falls gewünscht)
        if live == "False":
            los = los[los.asynch == 1]

        # topics: Angebote löschen, die nicht den gewählten Themen entsprechen
        if topic.lower() == 'egal': 
            res = ""
            for x in los['URL']:
                res += x
                res += "<br>"
            return dispatcher.utter_message(res)
        else:
            # für alle Lernangebote:
            for index, row in los.iterrows():
                no_match = True
                topics_lo = (row.topics).split(",")
                # für alle Themen des Lernangebots:
                for to_lo in topics_lo:
                    # vergleiche das angegebene Thema auf Übereinstimmung mit der Exceltabelle
                    if topic.lower() == to_lo.lower():
                        no_match = False
                # wenn es keine Übereinstimmung gibt entferne das Lernangebot aus der Liste
                if no_match: los.drop(index, inplace = True)

        # gebe die namen aller Lernangebote zurück, die übrig geblieben sind.
        if len(los['URL'])==0: dispatcher.utter_message("Es konnte leider kein passendes Lernangebot gefunden werden.")
        else: 
            res = ""
            for x in los['URL']:
                res += x
                res += "<br>"
            return dispatcher.utter_message(res)

class ActionRestart(Action):

    def name(self) -> Text:
            return "action_restart"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # custom behavior
        dispatcher.utter_message(response="utter_restart")
        return [Restarted()]
        

class ValidateCourseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_course_form"

    def validate_language(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate language"""
        if slot_value.lower() == "englisch":
            dispatcher.utter_message(text=f"Alles klar, dann merke ich mir Englisch für die weitere Kurssuche.")
            return {"startdate": slot_value}
        if slot_value.lower() == "deutsch":
            dispatcher.utter_message(text=f"Alles klar, dann merke ich mir Deutsch für die weitere Kurssuche.")
            return {"startdate": slot_value}
        if tracker.get_intent_of_latest_message() == "undecided":
            dispatcher.utter_message(text=f"Alles klar, für die weitere Kurssuche merke ich mir beide Sprachen.")
        else:
            dispatcher.utter_message(text=f"Ich habe die Sprache leider nicht erkannt, bitte schreib sie mir nochmal.")
            return {"startdate": None}
