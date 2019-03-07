import unittest
from util import ApiError 
from server import server
class TestApiError(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.context = server.app_context()

    def testError(self):
        error = ApiError("some message", payload={"error": "this is an error"})
        with self.context:
            res,status = error.get_response()
            self.assertEqual(status, 400, "status should be 400")
            self.assertEqual(res.is_json, True)
            self.assertEqual(res.get_json(), {"message": "some message", "error": "this is an error"})