#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Odarchenko N.D.'

import os
import datetime
import gobject
import pygtk

pygtk.require('2.0')
import gtk


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

        # rate $ per hour
        self.rate = 10

        # program's work time
        self.timer_start = 0
        # time from the last rest or beginning of resting (if user is resting now)
        self.timer_work = 0

        self.widget_showed = False

        self.timer_label = gtk.Label(u'Время с момента запуска: 0 сек.')
        self.rate_entry = gtk.Entry(6)
        self.button_update_rate = gtk.Button(stock=u'Ок')
        self.label_rate2 = gtk.Label(u'Заработано: 0.00')
        self.button_widget = gtk.Button(stock=u'Показать виджет')
        self.button_unset_rate = gtk.Button(stock=u'Обнулить счетчик')
        self.work_time_all = gobject.timeout_add(1000, self.every_second)
        self.popup = gtk.Window(gtk.WINDOW_POPUP)
        self.progressbar = gtk.ProgressBar()

        app_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        app_window.set_size_request(450, 200)
        app_window.set_border_width(10)
        app_window.set_resizable(False)
        app_window.set_title(u'Береги глаза, делай перерывы')
        app_window.connect("delete_event", lambda w, e: gtk.main_quit())
        label = gtk.Label(u'<span size="10500"><b>Не забывай делать перевы</b></span>')

        app_window.set_icon_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icon.png'))
        v_box_app = gtk.VBox(False, 0)
        app_window.add(v_box_app)
        v_box_app.show()

        label.set_use_markup(True)
        h_box = gtk.HBox(False, 0)
        h_box.pack_start(label)
        label.show()

        button_rest = gtk.Button(stock=u'Сделать перерыв сейчас')
        button_rest.connect("clicked", lambda w: self.rest())
        button_rest.set_flags(gtk.CAN_DEFAULT)
        h_box.pack_start(button_rest)

        button_rest.show()
        h_box.show()
        v_box_app.pack_start(h_box, True)

        # Place after association to hbox/vbox to avoid the following error:
        # GtkWarning: gtkwidget.c:5460: widget not within a GtkWindow
        button_rest.grab_default()

        h_box2 = gtk.HBox(False, 0)
        h_box2.pack_start(self.timer_label)
        self.timer_label.show()
        h_box2.show()
        v_box_app.add(h_box2)

        label_start_widget = gtk.Label(u'<b>Для оплачиваемой работы:</b>')
        label_start_widget.set_use_markup(True)
        h_box = gtk.HBox(False, 0)
        h_box.pack_start(label_start_widget)
        label_start_widget.show()
        h_box.show()
        v_box_app.add(h_box)

        v_box2 = gtk.VBox(True, 0)
        v_box2.show()

        label_rate = gtk.Label(u'Почасовой тариф ')
        h_box = gtk.HBox(False, 0)
        v_box2.add(h_box)
        h_box.pack_start(label_rate, False)
        label_rate.show()

        self.rate_entry.set_width_chars(6)
        self.rate_entry.set_text(str(self.rate))
        h_box.pack_start(self.rate_entry, False, False)
        self.rate_entry.show()
        self.rate_entry.connect('focus-out-event', lambda w, e: self.read_rate())
        self.button_update_rate.connect("clicked", lambda w: self.read_rate())
        h_box.pack_start(self.button_update_rate, False, False)
        self.button_update_rate.show()
        h_box.pack_start(self.label_rate2)
        self.label_rate2.show()
        self.button_widget.connect("clicked",
                                   lambda w: self.hide_widget() if self.widget_showed else self.show_widget())
        self.button_widget.set_flags(gtk.CAN_DEFAULT)

        h_box.show()
        v_box_app.pack_start(v_box2, False, False)

        h_box = gtk.HBox(False, 0)
        self.button_unset_rate.connect("clicked", lambda w: self.timer_clear())
        h_box.pack_start(self.button_unset_rate, False)
        self.button_unset_rate.show()

        h_box.pack_start(self.button_widget)
        self.button_widget.show()

        v_box_app.add(h_box)
        h_box.show()
        self.button_widget.grab_default()

        app_window.set_position(gtk.WIN_POS_MOUSE)
        app_window.show()

        s = app_window.get_screen()
        m = s.get_monitor_at_window(s.get_active_window())
        monitor = s.get_monitor_geometry(m)

        self.init_rest_dialog(monitor.width, monitor.height - 50)

        self.widget = TimerWidget(monitor.width - 200, monitor.height - 100)

    def init_rest_dialog(self, width, height):
        self.popup.set_border_width(10)
        self.popup.set_title(u'Береги глаза, делай перерывы')
        self.popup.set_position(gtk.WIN_POS_CENTER)
        self.popup.set_resizable(False)

        self.popup.set_size_request(width, height)
        self.popup.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000000'))
        v_box_app_p = gtk.VBox(False)
        self.popup.add(v_box_app_p)
        v_box_app_p.pack_start(self.progressbar, False, True, 0)
        self.progressbar.set_text(u'Перерыв')
        self.progressbar.show()

        popup_label = gtk.Label(u'<span size="30000">Пора сделать перерыв!</span>')
        popup_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        popup_label.set_use_markup(True)
        h_box = gtk.HBox(False, 0)
        h_box.pack_start(popup_label, True, False, 100)
        popup_label.show()

        button_postpone1 = gtk.Button(stock=u'Отложить перерыв на 3 мин.')
        button_postpone1.connect("clicked", lambda w: self.postpone())
        button_postpone1.set_flags(gtk.CAN_DEFAULT)

        h_box.pack_start(button_postpone1, False, False, 0)

        button_postpone2 = gtk.Button(stock=u'Отложить перерыв на 50 мин.')
        button_postpone2.connect("clicked", lambda w: self.work())
        button_postpone2.set_flags(gtk.CAN_DEFAULT)
        h_box.pack_start(button_postpone2, False, False, 200)

        button_postpone1.show()
        button_postpone2.show()
        h_box.show()
        v_box_app_p.pack_start(h_box, fill=False)
        v_box_app_p.show()

        # Place after association to hbox/vbox to avoid the following error:
        # GtkWarning: gtkwidget.c:5460: widget not within a GtkWindow
        button_postpone1.grab_default()

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
        if self.widget.real_work_timer_on and time2rest != 0:
            self.widget.real_work += 1
            self.update_money(float(self.rate) * self.widget.real_work / 3600)

        self.timer_label.set_text(u'Время с момента запуска: ' + self.time_format(self.timer_start)
                                  + u"\nДо следующего перерыва: " + self.time_format(time2rest))
        self.work_time_all = gobject.timeout_add(1000, self.every_second)

    def show_widget(self):
        self.widget_showed = True
        self.button_widget.set_label(u' Скрыть виджет  ')
        self.widget.show()
        self.read_rate()

    def hide_widget(self):
        self.widget_showed = False
        self.button_widget.set_label(u'Показать виджет')
        self.widget.hide()
        self.read_rate()

    def read_rate(self):
        try:
            self.rate = float(self.rate_entry.get_text())
        except ValueError:
            self.rate_entry.set_text(str(self.rate))

    def update_money(self, money):
        my_money = "%6.2f" % money
        self.label_rate2.set_text(u'Заработано: ' + my_money)
        if self.widget_showed:
            w_text = self.time_format(self.widget.real_work) + "\t" + my_money
            if not self.widget.big and len(w_text) > 15:
                self.widget.set_big(True)
            self.widget.widget_label.set_text(w_text)

    def timer_clear(self):
        self.widget.real_work = 0
        self.update_money(0)

    @staticmethod
    def time_format(tm):
        dt = datetime.datetime.utcfromtimestamp(tm)
        days = tm // 86400
        if days:
            return str(days) + u'дн. ' + dt.strftime('%H:%M:%S')
        return dt.strftime('%H:%M:%S')


class TimerWidget(gtk.Window):
    def __init__(self, position_x=0, position_y=0):
        super(TimerWidget, self).__init__(gtk.WINDOW_POPUP)
        self.widget_moving = False
        self.widget_moving_coord = None
        self.set_border_width(1)
        self.set_title(u'Таймер рабочего времени')
        self.move(position_x, position_y)
        self.set_resizable(True)
        self.set_can_focus(True)
        self.set_opacity(0.6)
        self.set_size_request(120, 60)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#004F00'))
        v_box = gtk.VBox(False)
        self.add(v_box)
        self.connect('button_press_event', self.widget_press_event)
        self.connect('button_release_event', self.widget_release_event)
        self.connect('motion_notify_event', self.widget_motion_notify_event)
        self.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.LEAVE_NOTIFY_MASK
                        | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK
                        | gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK)
        h_box = gtk.HBox(False, 0)
        button_timer = gtk.ToggleButton(u'Таймер')
        button_timer.connect("toggled", self.widget_timer_toggled)
        button_timer.set_flags(gtk.CAN_DEFAULT)
        h_box.pack_start(button_timer)
        button_timer.show()
        h_box.show()
        v_box.pack_start(h_box)
        self.widget_label = gtk.Label(u'<small>Нажмите на кнопку</small>')
        self.widget_label.set_use_markup(True)
        self.widget_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        h_box = gtk.HBox(False, 0)
        h_box.pack_start(self.widget_label)
        h_box.show()
        v_box.pack_start(h_box)
        self.widget_label.show()
        v_box.show()

        # Place after association to horizontal_box/v_box to avoid the following error:
        # GtkWarning: gtkwidget.c:5460: widget not within a GtkWindow
        button_timer.grab_default()

        # work for money
        self.real_work = 0
        self.real_work_timer_on = False
        # large window mode
        self.big = False

    def widget_timer_toggled(self, w):
        self.real_work_timer_on = not self.real_work_timer_on
        self.modify_bg(gtk.STATE_NORMAL,
                       gtk.gdk.color_parse('#4F0000' if self.real_work_timer_on else '#004F00'))

    def widget_press_event(self, w, e):
        self.widget_moving = True
        self.widget_moving_coord = -int(e.x), -int(e.y)

    def widget_motion_notify_event(self, w, e):
        if self.widget_moving:
            x, y = self.get_position()
            x2, y2 = self.widget_moving_coord
            self.move(x + int(e.x) + x2, y + int(e.y) + y2)

    def widget_release_event(self, w, e):
        self.widget_moving = False

    def set_big(self, value):
        self.big = value
        if value:
            self.set_size_request(150, 60)
        else:
            self.set_size_request(120, 60)


if __name__ == "__main__":
    MainWindow()
    gtk.main()