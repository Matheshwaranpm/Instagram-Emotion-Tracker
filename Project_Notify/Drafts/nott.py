import pywintypes
from win10toast import ToastNotifier

toast = ToastNotifier()

toast.show_toast("This is a Notification","You got it!",duration=5)