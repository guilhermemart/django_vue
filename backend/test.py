import main

class fake_request():
    data = {"id": 1642602580, "thumb_up": False, "thumb_down": True, "notes": "abcd"}

def test_update_alert():
    request_fake = fake_request.data
    main.update_alerts_by_id(request_fake)


test_update_alert()