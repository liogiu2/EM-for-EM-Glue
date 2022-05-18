import unittest
from unittest.mock import patch
import responses
import json
from experience_manager import ExperienceManager
from platform_communication import PlatformCommunication

class TestEMPlatformCommunication(unittest.TestCase):

    def setUp(self):
        self.protocol_messages = {
            "PHASE_1" : 
            {
                "message_1" : "start of communication. name:",
                "message_2" : "inizialization completed. wait preparation environment."
            },
            "PHASE_2" : 
            {
                "message_3" : "start of communication. name:",
                "message_4" : "inizialization completed. Request for initial state of environment."
            },
            "PHASE_3" : 
            {
                "message_5" : "request domain and problem",
                "message_6" : "domain and problem",
                "message_7" : "domain and problem"
            },
            "PHASE_4" : 
            {
                "message_8" : "received domain and problem. request links for communication",
                "message_9" : "receved. start communication on links",
                "message_10" : "links"
            }
        }
        
    @responses.activate
    def test_platform_handshake(self):
        message = {'text': self.protocol_messages["PHASE_1"]["message_2"]}
        responses.add(responses.GET, 'http://127.0.0.1:8080/get_protocol_messages', json=self.protocol_messages)
        responses.add(responses.GET, 'http://127.0.0.1:8080/inizialization_em', json=message, status=200)
        message = {
            'text': self.protocol_messages["PHASE_3"]["message_7"],
            'domain': 'domain example',
            'problem': 'problem example'
        }
        responses.add(responses.GET, 'http://127.0.0.1:8080/inizialization_em', json=message, status=200)
        message = {
            'text': self.protocol_messages["PHASE_4"]["message_10"],
            'get_message_url': 'url_in',
            'add_message_url': 'url_out'
        }
        responses.add(responses.GET, 'http://127.0.0.1:8080/inizialization_em', json=message, status=200)
        responses.add(responses.GET, 'http://127.0.0.1:8080/protocol_phase', body="PHASE_3", status=200)
        with patch.object(PlatformCommunication.__wrapped__ , 'is_platform_online') as mock_is_platform_online:
            mock_is_platform_online.return_value = True
            em = ExperienceManager()
            em.start_platform_communication()
        self.assertTrue(True)
        self.assertEqual(responses.calls[1].request.params, {"text": "start of communication. name: Experience Manager"})
        self.assertEqual(responses.calls[3].request.params, {"text": "request domain and problem"})
        self.assertNotEqual(em.PDDL_domain_text, "")
        self.assertNotEqual(em.PDDL_problem_text, "")
        self.assertEqual(responses.calls[4].request.params, {"text": "received domain and problem. request links for communication"})
        self.assertNotEqual(em.platform_communication.receive_message_link, "")
        self.assertNotEqual(em.platform_communication.send_message_link, "")

if __name__ == '__main__':
    unittest.main()