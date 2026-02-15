import caldav
from icalendar import Calendar, Event, vText
from datetime import datetime, timedelta
import pytz
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class PofficeCalendar:
    def __init__(self, username, password, base_url="https://mail.poffice.online/SOGo/dav/"):
        self.username = username
        self.password = password
        self.base_url = base_url

    def _get_calendar(self):
        client = caldav.DAVClient(url=self.base_url, username=self.username, password=self.password)
        principal = client.principal()
        calendars = principal.calendars()
        if not calendars:
            raise Exception("No calendars found")
        return calendars[0]

    def add_event(self, summary, description, start_time, duration_minutes=60, location=None):
        try:
            calendar = self._get_calendar()
            cal = Calendar()
            cal.add('prodid', '-//Poffice Automation//poffice.online//')
            cal.add('version', '2.0')
            
            event = Event()
            event.add('summary', summary)
            event.add('description', description)
            if location:
                event.add('location', location)
            event.add('dtstart', start_time)
            event.add('dtend', start_time + timedelta(minutes=duration_minutes))
            event.add('dtstamp', datetime.now(pytz.utc))
            event.add('uid', str(uuid.uuid4()))
            
            cal.add_component(event)
            calendar.save_event(cal.to_ical())
            return {"status": "success", "message": f"Event '{summary}' added"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_events(self, start=None, end=None):
        try:
            calendar = self._get_calendar()
            if not start:
                start = datetime.now(pytz.utc)
            if not end:
                end = start + timedelta(days=7)
            
            events = calendar.date_search(start, end)
            results = []
            for event in events:
                ical = Calendar.from_ical(event.data)
                for component in ical.walk():
                    if component.name == "VEVENT":
                        results.append({
                            "uid": str(component.get('uid')),
                            "summary": str(component.get('summary')),
                            "start": component.get('dtstart').dt.isoformat(),
                            "end": component.get('dtend').dt.isoformat() if component.get('dtend') else None,
                            "description": str(component.get('description'))
                        })
            return {"status": "success", "events": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_event(self, uid):
        try:
            calendar = self._get_calendar()
            event = calendar.event_by_uid(uid)
            event.delete()
            return {"status": "success", "message": f"Event {uid} deleted"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_event(self, uid, summary=None, description=None, start_time=None, duration_minutes=None):
        try:
            calendar = self._get_calendar()
            event_obj = calendar.event_by_uid(uid)
            ical = Calendar.from_ical(event_obj.data)
            
            for component in ical.walk():
                if component.name == "VEVENT":
                    if summary: component.replace('summary', summary)
                    if description: component.replace('description', description)
                    if start_time: 
                        component.replace('dtstart', start_time)
                        if duration_minutes:
                             component.replace('dtend', start_time + timedelta(minutes=duration_minutes))
                    elif duration_minutes:
                        old_start = component.get('dtstart').dt
                        component.replace('dtend', old_start + timedelta(minutes=duration_minutes))
            
            event_obj.data = ical.to_ical()
            event_obj.save()
            return {"status": "success", "message": f"Event {uid} updated"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def send_invite(self, smtp_user, smtp_pass, to_email, summary, description, start_time, duration_minutes=60, location=None):
        msg = MIMEMultipart('mixed')
        msg['Reply-To'] = smtp_user
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = f"Invitation: {summary}"
        cal = Calendar()
        cal.add('prodid', '-//Poffice Automation//poffice.online//'); cal.add('version', '2.0'); cal.add('method', 'REQUEST')
        event = Event()
        event.add('summary', summary); event.add('description', description)
        if location: event.add('location', location)
        event.add('dtstart', start_time); event.add('dtend', start_time + timedelta(minutes=duration_minutes))
        event.add('dtstamp', datetime.now(pytz.utc)); event.add('uid', str(uuid.uuid4())); event.add('priority', 5)
        event.add('attendee', f"MAILTO:{to_email}", extra_params={'RSVP': 'TRUE'})
        event.add('organizer', f"MAILTO:{smtp_user}")
        cal.add_component(event)
        part_text = MIMEText(f"You are invited to: {summary}\n\nDescription: {description}", 'plain')
        msg.attach(part_text)
        part_ics = MIMEText(cal.to_ical().decode("utf-8"), 'calendar; method=REQUEST')
        part_ics.add_header('Content-class', 'urn:content-classes:calendarmessage')
        part_ics.add_header('Filename', 'invite.ics'); part_ics.add_header('Content-Disposition', 'attachment; filename=invite.ics')
        msg.attach(part_ics)
        try:
            server = smtplib.SMTP("mail.poffice.online", 587); server.starttls(); server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, to_email, msg.as_string()); server.quit()
            return {"status": "success"}
        except Exception as e: return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import sys, os
    USER = os.getenv("POFFICE_EMAIL", "admin@poffice.online")
    PASS = os.getenv("POFFICE_PASSWORD", "Poffice2025")
    cal_manager = PofficeCalendar(USER, PASS)
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "add":
            start_dt = datetime.strptime(sys.argv[4], "%Y-%m-%d %H:%M").replace(tzinfo=pytz.utc)
            print(cal_manager.add_event(sys.argv[2], sys.argv[3], start_dt))
        elif action == "list":
            print(cal_manager.list_events())
        elif action == "delete":
            print(cal_manager.delete_event(sys.argv[2]))
        elif action == "invite":
            start_dt = datetime.strptime(sys.argv[5], "%Y-%m-%d %H:%M").replace(tzinfo=pytz.utc)
            print(cal_manager.send_invite(USER, PASS, sys.argv[2], sys.argv[3], sys.argv[4], start_dt))
