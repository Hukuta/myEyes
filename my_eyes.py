#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Odarchenko N.D.'

import os
import datetime
import gobject
import pygtk
pygtk.require('2.0')
import gtk


def time_format(tm):
    dt = datetime.datetime.utcfromtimestamp(tm)
    days = tm // 86400
    if days:
        return str(days) + u'дн. ' + dt.strftime('%H:%M:%S')
    return dt.strftime('%H:%M:%S')


class MainWindow:
    def __init__(self):
        # Interval between breaks 50 min
        self.interval = 3000
        # interval if postponed 3 min
        self.interval2 = 180
        # breaks time 4 min
        self.break_time = 240

        # 0 -> work, 1 -> rest, 2 -> postponed
        self.state = 0

        app_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        app_window.set_size_request(450, 100)
        app_window.set_border_width(10)
        app_window.set_title(u'Береги глаза, делай перерывы')
        app_window.connect("delete_event", lambda w, e: gtk.main_quit())
        label = gtk.Label(u'<span size="10500"><b>Не забывай делать перевы.</b></span>')
        self.timer_label = gtk.Label(u'Рабочее время с момента запуска: 0 сек.')
        self.timer_start = 0
        self.timer_work = 0

        app_window.set_icon_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icon.png'))

        vbox_app = gtk.VBox(False, 0)
        app_window.add(vbox_app)
        vbox_app.show()

        label.set_use_markup(True)
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(label)
        label.show()

        button_rest = gtk.Button(stock=u'Сделать перерыв сейчас')
        button_rest.connect("clicked", lambda w: self.rest())
        button_rest.set_flags(gtk.CAN_DEFAULT)
        hbox.pack_start(button_rest)

        button_rest.show()
        hbox.show()
        vbox_app.add(hbox)

        # Place after association to hbox/vbox to avoid the following error:
        # GtkWarning: gtkwidget.c:5460: widget not within a GtkWindow
        button_rest.grab_default()

        hbox2 = gtk.HBox(False, 0)
        hbox2.pack_start(self.timer_label)
        self.timer_label.show()
        hbox2.show()
        vbox_app.add(hbox2)

        app_window.set_position(gtk.WIN_POS_MOUSE)
        app_window.show()

        self.work_time_all = gobject.timeout_add(1000, self.every_second)

        self.popup = gtk.Window(gtk.WINDOW_POPUP)

        self.popup.set_border_width(10)
        self.popup.set_title(u'Береги глаза, делай перерывы')
        self.popup.set_position(gtk.WIN_POS_CENTER)
        self.popup.set_resizable(False)
        s = app_window.get_screen()
        m = s.get_monitor_at_window(s.get_active_window())
        monitor = s.get_monitor_geometry(m)
        self.popup.set_size_request(monitor.width, monitor.height - 50)
        self.popup.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000000'))

        vbox_app_p = gtk.VBox(False)
        self.popup.add(vbox_app_p)

        self.progressbar = gtk.ProgressBar()
        vbox_app_p.pack_start(self.progressbar, False, True, 0)
        self.progressbar.set_text(u'Перерыв')
        self.progressbar.show()

        self.popup_label = gtk.Label(u'<span size="30000">Пора сделать перерыв!</span>')
        self.popup_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        self.popup_label.set_use_markup(True)
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(self.popup_label, True, False, 100)
        self.popup_label.show()

        button_postpone1 = gtk.Button(stock=u'Отложить перерыв на 3 мин.')
        button_postpone1.connect("clicked", lambda w: self.postpone())
        button_postpone1.set_flags(gtk.CAN_DEFAULT)

        hbox.pack_start(button_postpone1, False, False, 0)

        button_postpone2 = gtk.Button(stock=u'Отложить перерыв на 50 мин.')
        button_postpone2.connect("clicked", lambda w: self.work())
        button_postpone2.set_flags(gtk.CAN_DEFAULT)
        hbox.pack_start(button_postpone2, False, False, 200)

        button_postpone1.show()
        button_postpone2.show()
        hbox.show()
        vbox_app_p.pack_start(hbox, fill=False)
        vbox_app_p.show()

        # Place after association to hbox/vbox to avoid the following error:
        # GtkWarning: gtkwidget.c:5460: widget not within a GtkWindow
        button_postpone1.grab_default()

        return

    def rest(self):
        self.timer_work = 0
        self.state = 1
        self.popup.show()

    def work(self):
        self.timer_work = 0
        self.state = 0
        self.popup.hide()

    def postpone(self):
        self.timer_work = 0
        self.state = 3
        self.popup.hide()

    def every_second(self):
        self.timer_start += 1
        self.timer_work += 1
        time2rest = 0
        if self.state == 0:
            time2rest = self.interval - self.timer_work
            if time2rest <= 0:
                # going to rest
                self.rest()
                time2rest = 0
        elif self.state == 1:
            time2work = self.break_time - self.timer_work
            if time2work <= 0:
                # going to work
                self.work()
                #time2work = 0
            else:
                self.progressbar.set_fraction(1 - float(time2work) / self.break_time)
                progress_str = u'Перерыв закончится через %s мин. %s сек.' % (time2work // 60, time2work % 60)
                self.progressbar.set_text(progress_str)
        else:
            time2rest = self.interval2 - self.timer_work
            if time2rest <= 0:
                # going to rest
                self.rest()
                time2rest = 0

        self.timer_label.set_text(u'Рабочее время с момента запуска: ' + time_format(self.timer_start)
                                  + u"\nДо следующего перерыва: " + time_format(time2rest))
        self.work_time_all = gobject.timeout_add(1000, self.every_second)


if __name__ == "__main__":
    MainWindow()
    gtk.main()