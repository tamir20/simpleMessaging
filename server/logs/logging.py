import win32evtlog
import win32evtlogutil

# i use this weird combination of app name and event id because
# it will be easier to view later on the event viewr.
# for more information read here:
# https://www.jitbit.com/alexblog/266-writing-to-an-event-log-from-net-without-the-description-for-event-id-nonsense/
APP_NAME = ".NET Runtime"
EVENT_ID = 1000

def log_to_event_viewer_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log error event
            win32evtlogutil.ReportEvent(
                APP_NAME,
                EVENT_ID,  # Event ID (customize as needed)
                eventType=win32evtlog.EVENTLOG_ERROR_TYPE,
                strings=[f"Error: {str(e)}"],
            )
            raise

    return wrapper

def log_to_event_viewer(log: str) -> None:
    win32evtlogutil.ReportEvent(
        APP_NAME,
        EVENT_ID,  # Event ID (customize as needed)
        eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
        strings=[log],
    )
