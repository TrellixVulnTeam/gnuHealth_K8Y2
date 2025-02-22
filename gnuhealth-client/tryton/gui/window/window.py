# This file is part of the GNU Health GTK Client.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


class Window(object):

    hide_current = False
    allow_similar = False

    def __init__(self, hide_current=False, allow_similar=True):
        Window.hide_current = hide_current
        Window.allow_similar = allow_similar

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        Window.hide_current = False
        Window.allow_similar = False

    @staticmethod
    def create(model, **attributes):
        from tryton.gui import Main
        if model:
            from form import Form
            win = Form(model, **attributes)
        else:
            from board import Board
            win = Board(model, **attributes)
        win.icon = attributes.get('icon')
        Main.get_main().win_add(win, hide_current=Window.hide_current,
            allow_similar=Window.allow_similar)

    @staticmethod
    def create_wizard(action, data, direct_print=False, email_print=False,
            email=None, name='', context=None, icon=None, window=False):
        from tryton.gui import Main
        from wizard import WizardForm, WizardDialog
        if window:
            win = WizardForm(name=name)
            win.icon = icon
            Main.get_main().win_add(win, Window.hide_current)
        else:
            win = WizardDialog(name=name)
        win.run(action, data, direct_print=direct_print,
            email_print=email_print, email=email, context=context)
